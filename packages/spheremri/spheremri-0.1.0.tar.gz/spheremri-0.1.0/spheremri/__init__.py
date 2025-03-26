"""
sphereMRI: PyPI package for MRI quality rating
"""

# Disable DINOv2 xFormers warnings - this must be done before any other imports
import os
os.environ['DINOV2_XFORMERS_DISABLED'] = '1'

__version__ = '0.1.0'
