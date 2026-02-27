"""b) Contrastive learning pre-training for classification: Contrastive learning trains
models to group similar data points closer in an embedding space and push dissimilar
ones apart. For this task, you should first implement a contrastive learning pre-training
strategy (you can choose the one you prefer) using the Contrastive set you created
in task 2.3.1. You can then make the encoder fixed, use its features to train another
classification head for the nuclei classification task. The hypothesis is that contrastive
learning helps the network learn relevant class differences on large unlabeled data and
subsequently potentially improving accuracy for small annotated datasets.
"""