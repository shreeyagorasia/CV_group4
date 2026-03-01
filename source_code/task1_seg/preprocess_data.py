"""
Preprocess data: 
1. Drop alpha channel from images
2. Convert GeoJSON masks to rasterized masks - shape (1024,1024)
3. create only 3 classes: Tumor = 1, Stroma = 2, Other = 0
4. For each split, load image to get H,W 
    5. load matching GeoJSON file
    6. Convert polygons, to pixel map. 
    7. save mask 
8. End = for each image orginal tif is input image, create a .npy mask file, 
    then training becomes loading image, loading mask, training Unet or autoencoder
"""