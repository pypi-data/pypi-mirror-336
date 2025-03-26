"""
Command line interface for sphereMRI
"""
# Disable DINOv2 xFormers warnings - must be set before other imports
import os
os.environ['DINOV2_XFORMERS_DISABLED'] = '1'

import argparse
import sys
import torch
from pathlib import Path

from spheremri.rater import NiftiQualityRater
from spheremri.model_selector import ModelSelector
import pkg_resources

def rate_command(args):
    """
    Run the rating command
    
    Args:
        args: Command line arguments
    """
    print(f"Rating image: {args.input}")
    
    # Set device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
     
    # Load model
    model_selector = ModelSelector()
    model = model_selector.get_model()
    
    model_path = pkg_resources.resource_filename('spheremri', 'dinov2s.pt')
    model.load_state_dict(torch.load(model_path, map_location=device))
    
    # Determine contrast type
    contrast = 't1' if args.t1 else 'tse'
    if args.t1:
        print("Using T1 contrast mode")
    else:
        print("Using TSE contrast mode (default)")
    
    # Determine appropriate slice index if not specified
    if args.slice_idx is None:
        # Use slice_idx=1 for T1 and slice_idx=-1 for TSE
        slice_idx = 1 if args.t1 else -1
        print(f"Automatically setting slice_idx={slice_idx} based on contrast")
    else:
        slice_idx = args.slice_idx
    
    # Create rater
    rater = NiftiQualityRater(
        model=model,
        device=device,
        contrastive=args.contrastive,
        num_anchor_images=args.num_anchor_images,
        contrast=contrast
    )

    # Create anchor embedding if reference directory provided
    if args.reference_dir:
        print(f"Creating anchor embedding from: {args.reference_dir}")
        rater.create_anchor_embedding(args.reference_dir, slice_idx=slice_idx)
    else:
        # Let the rater load the appropriate anchor embedding based on contrast
        rater.load_prebuilt_anchor()
    
    # Rate the image
    score, embedding, distance = rater.rate_image(args.input, slice_idx=slice_idx)
    
    print(f"Quality score: {score:.4f}")
    
    # Save detailed results if output directory is provided
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Save the score to a text file
        with open(output_dir / "score.txt", "w") as f:
            f.write(f"{score:.6f}\n")
        
        # Save the embedding as tensor
        torch.save(embedding, output_dir / "embedding.pt")
        
        print(f"Results saved to: {output_dir}")
    
    return score


def main():
    """Main entry point for the CLI"""
    # Suppress PyTorch/DINOv2 warnings
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    
    parser = argparse.ArgumentParser(description="sphereMRI: MRI Quality Rating Tool")
    
    # Main arguments (no subcommands)
    parser.add_argument("-i", "--input", required=True, help="Input NIfTI file to rate")
    parser.add_argument("-r", "--reference-dir", help="Directory with reference quality images")
    parser.add_argument("-o", "--output-dir", help="Output directory for detailed results")
    parser.add_argument("-c", "--checkpoint", help="Path to model checkpoint")
    parser.add_argument("--contrastive", default="angular", choices=["angular", "euclidean"], help="Contrastive method")
    parser.add_argument("--slice-idx", type=int, default=-1, help="Slice index. Slanted TSE uses -1 which is default.")
    parser.add_argument("--num-anchor-images", type=int, default=5, help="Number of anchor images to use")
    parser.add_argument("--t1", action="store_true", help="Use T1 contrast mode (default is TSE)")
    
    args = parser.parse_args()
    
    rate_command(args)


if __name__ == "__main__":
    sys.exit(main())
