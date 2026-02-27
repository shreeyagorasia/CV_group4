### Task 1 Segmentation

- **(a) UNet end-to-end**:  input to the UNet model should be the image, and the output will be the image segmentation mask
- **(b) autoencoder-pretrained segmentation**: first train an autoencoder on the raw images (without labels) to reconstruct the image itself. You can then make the autoencoder’s encoder fixed, use its features to train another decoder for the image segmentation task
- **(c) Evaluation of method a and b** 
- Intersection over Union (IoU), Dice coefficient (F1 score for segmentation), or Pixel Accuracy, as appropriate for the dataset and its multi-class nature
- The baseline’s average Dice coefficient across the three categories is 0.4670, and your best-performing method is supposed to be above the baseline (N.B. we are more interested in the motivations behind your implementation choices)
- The baseline has∼ 125M trainable parameters. Report the trainable parameter of your own solutions and comment on such a comparison.

### Task 2 classification: 
- **(a) Dataset creation**
  - Training: extract 2500 patches per class from the originally provided training set folder.
  - Validation: extract 700 patches per class from the originally provided validation set folder
  - Contrastive set: decide how many patches per class from the originally provided training set folder you will like and extract them (be sure to prevent data leakage)
    - Read .tif full images from training split
    - Read nuclei annotations from GeoJSON
    - For each annotated nucleus: Get its center coordinate, Crop a 100×100 patch centered on it, Zero-pad if near image border (just like test set description) 
    - Label it based on its class
    - Repeat until: 2500 per class (train), 700 per class (val) to give balanced supervised dataset
- **(b) end-to-end classification nueral net:** 
  - Select and implement your classification network, and train it on the training dataset you have created in task 2.3.1. The input to the classification model should be the image, and the output will be the corresponding nucleus class.
    - take patch, feed into cnn , output classes 1,2,3, train with cross entropy. output metrics like accuracy precision, recall-multiclass.
    - baseline’s average accuracy across the 3 categories is 0.7083, try to answer motivations why ours is better 
    - baseline has∼ 5M trainable parameters. Report the trainable parameter of your own solutions and comment on such a comparison.
- **(c) contrastive-pretrained classifier**: does not use labels initally. 
  - take constrative data set, training split 
  - for each patch create two augemented verions 
    - same patch, mebddings close, different patches, embeddings far. 
    - after training freeze qeights, add classification head, train head using labelled supervised dataset. evaluate on test set. 
- **(d) Evaluation**: 
  - test classificaiton on test set (supervised and constrative pre-trained): accuracy, precision, recall, confusion, compare to baselines 0.7083, parameter 5m 
  - Evaluate the quality of the obtained latent space for the contrastive learning-based part. You could use both visual or numerical evaluations.(Use t-SNE or UMAP to visualize 2D projection), slhoutte score, knn classiicaiton accuracy in embedding space. 
  - b) Compare the performance of your two classification models. Which architecture or approach achieves the best metrics? How does pre-training influence the results?
  - c) Does the nature of the samples (i.e., primary vs metastatic) impact performance? Please comment.