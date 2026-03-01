"""
familiarize yourself with the dataset structure 
 - (train 163 / validation 20 / test 22)
 - image dimensions shape = (1024, 1024, 4), RGBA images, alpha = opaqueness  
 - mask formats = GeoJSON = labels, outlines a tissue region. 
    - images = .tif format  1024, 1024, 4). 
 - label classes (Tissue, Tissue Stroma, Other = Tissue Blood Vessel, Tissue Epidermis, Tissue White Background and Tissue Necrosi)
"""

from pathlib import Path
import tifffile as tiff
import json
import numpy as np
from collections import Counter

all_classes = set()
class_counts = Counter()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT = PROJECT_ROOT / "data" / "Dataset_Splits"

for split in ["train", "validation", "test"]:

    print("\n", split.upper())

    image_dir = ROOT / split / "image"
    tissue_dir = ROOT / split / "tissue"

    tif_files = sorted(image_dir.rglob("*.tif"))
    geo_files = sorted(tissue_dir.rglob("*.geojson"))

    print("Number of images:", len(tif_files))
    print("Number of label files:", len(geo_files))

    # looking at ONE image per split
    if tif_files:
        img = tiff.imread(tif_files[0])
        print("Example image:", tif_files[0].name)
        print("Image shape:", img.shape)
        print("Image dtype:", img.dtype)
        print("Pixel min/max:", int(img.min()), int(img.max()))
        
        with open(geo_files[0]) as f:
            data = json.load(f)
        print(data["features"][0])

        # check if selected image is RGBA
        if img.ndim == 3 and img.shape[2] == 4:
            alpha = img[:, :, 3]
            print("Alpha min/max:", int(alpha.min()), int(alpha.max()))
            print("Unique alpha values:", len(np.unique(alpha)))


    # ---- scan ALL label files in this split ----
    for gf in geo_files:
        with open(gf) as f:
            data = json.load(f) # load GeoJSON and load as python dict

        # Each GeoJSON file contains a list of annotated regions under "features".
        # Each feature represents one labeled tissue region (a polygon)
        # inside the image, with:
        #   - geometry → the coordinates of the region
        #   - properties → metadata including the tissue class name.

        # loop through all features to extract the class labels and count no. each tissue type
        for feat in data.get("features", []): 
            props = feat.get("properties", {})
            if isinstance(props.get("classification"), dict):
                name = props["classification"].get("name", "")
            else:
                name = props.get("name", "") or props.get("class", "")

            if name:
                all_classes.add(name)
                class_counts[name] += 1

print("\n OVERALL DATASET LABEL CLASSES (ALL SPLITS)")
print("All unique tissue classes:")
for c in sorted(all_classes):
    print(" -", c)

print("\nTotal polygon count per class:")
for c, n in class_counts.most_common():
    print(f"{c}: {n}")



"""
1) Dataset Structure
Splits: Train: 163 images, Validation: 20 images, Test: 22 images 
Each split contains:
- image/      -> .tif image files
- tissue/     -> .geojson label files
Each image has exactly one matching GeoJSON label file.

2) Image Information
Image shape: (1024, 1024, 4)
Data type: uint8
Pixel range: approximately 0–255
There are 4 channels (RGBA).
Alpha channel:
- min/max: 255–255
- unique values: 1
-> Alpha channel is constant (fully opaque).
-> It contains no useful information.
-> We will drop channel 4 and use only RGB.
Final model input shape: (1024, 1024, 3)

3) Label Format
Labels are provided as GeoJSON polygon annotations, each polygon outlines a tissue region.
These are vector masks (describes regions using mathematical masks).
They must be converted into raster segmentation masks (grid of pixels representing class)
Convert into --> (1024, 1024) integer mask arrays.

4) Object-Level Class Distribution (Polygon Counts) - all unqiue classes found:
tissue_tumor: 636
tissue_stroma: 294
tissue_blood_vessel: 284
tissue_epidermis: 48
tissue_white_background: 15
tissue_necrosis: 11

Observations:
- Tumor is most common.
- Stroma and blood vessel moderate.
- Epidermis, necrosis, white background are rare.
- Likely class imbalance.

5) Required Class Mapping (Task Requirement)
Need to reduce to 3 classes:
Tumor 1  -> tissue_tumor
Stroma 2 -> tissue_stroma
Other 0  -> tissue_blood_vessel
           tissue_epidermis
           tissue_necrosis
           tissue_white_background

6) Problem Summary
This is a 3-class semantic segmentation task on 1024x1024 RGB images.
Images are small enough to train directly (no tiling required).
Dataset is relatively small (163 training images).
Labels must be rasterized from polygons to pixel masks.
Class imbalance is likely and may affect training.
"""