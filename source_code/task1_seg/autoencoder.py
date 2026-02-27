
"""
b) Autoencoder pre-training for segmentation: An autoencoder learns to compress
and reconstruct images. For this task, you should first train an autoencoder on the
raw images (without labels) to reconstruct the image itself. You can then make the
autoencoder’s encoder fixed, use its features to train another decoder for the image
segmentation task. The hypothesis is that pre-training helps the network learn rel-
evant low-level and mid-level features, accelerating subsequent segmentation training
and potentially improving accuracy.
"""

