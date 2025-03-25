(methods)=

# Methods

Lightly**Train** supports the following self-supervised learning methods:

- `dino`

  [DINO](https://arxiv.org/abs/2104.14294) is a popular self-supervised learning
  method that works well across various datasets, model architectures, and tasks.

- `distillation` (recommended)

  Distillation is a method that transfers knowledge from a pre-trained model, in particular a ViT-B/14 from [DINOv2](https://arxiv.org/pdf/2304.07193).

- `densecl` (experimental)

  [DenseCL](https://arxiv.org/abs/2011.09157) was developed for learning strong local
  image representations, particularly for detection and segmentation tasks.

- `simclr`

  [SimCLR](https://arxiv.org/abs/2002.05709) is a classic self-supervised learning
  method widely used as a baseline for model pre-training.
