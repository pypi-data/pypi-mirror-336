```{eval-rst}
.. image:: _static/lightly_train_light.svg
   :align: center
   :class: only-light

.. image:: _static/lightly_train_dark.svg
   :align: center
   :class: only-dark
```

*Build better computer vision models faster with self-supervised pre-training*

Lightly**Train** leverages self-supervised learning (SSL) and distillation from
foundation models to train computer vision models on large datasets **without labels**.
It provides simple Python, Command Line, and Docker interfaces to train models with
popular pretraining methods such as SimCLR, DINO or distillation from DINOv2.

## Why Lightly**Train**?

- 🚀 **Higher accuracy** – Pretrained models generalize better and achieve higher performance.
- 💸 **Cost efficiency** – Make use of unlabeled data instead of letting it go to waste.
- ⚡ **Faster convergence** – Pretraining with LightlyTrain speeds up learning and reduces compute time.
- 🖼️ **Better image embeddings** – Extract more meaningful features than with supervised models.
- 🏗️ **Stronger foundation** – A great starting point for downstream tasks like:
  - **Image classification**
  - **Object detection**
  - **Segmentation**
- 🔄 **Improved domain adaptation** – Self-supervised learning enables better adaptability to data shifts.

Lightly are the experts in computer vision pretraining and developed Lightly**Train** to
simplify model training for any task and dataset.

## How It Works

### Train a Model with SSL

```python
import lightly_train

lightly_train.train(
    out="out/my_experiment",            # Output directory
    data="my_data_dir",                 # Directory with images
    model="torchvision/resnet50",       # Model to train
)
```

This will pretrain a Torchvision ResNet-50 model using images from `my_data_dir` and the
DINO self-supervised learning method. All training logs, model exports, and checkpoints
are saved to the output directory at `out/my_experiment`.

The final model is exported to `out/my_experiment/exported_models/exported_last.pt` in
the default format of the used library. It can directly be used for
fine-tuning. Follow the [example](quick_start.md#fine-tune) to learn how to
fine-tune a model.

After training is complete, you can either use the exported model for fine-tuning,
or use the model to [generate image embeddings](#generate-image-embeddings).

### Generate Image Embeddings

```python
import lightly_train

lightly_train.embed(
    out="my_embeddings.pth",                                # Exported embeddings
    checkpoint="out/my_experiment/checkpoints/last.ckpt",   # LightlyTrain checkpoint
    data="my_data_dir",                                     # Directory with images
)
```

You can now use the generated embeddings for clustering, retrieval, or visualization
tasks.

The [quick start guide](#quick-start) shows in more detail how to install and use
Lightly**Train**.

## Features

- Train models on any image data without labels
- Train models from popular libraries such as [torchvision](https://github.com/pytorch/vision), [TIMM](https://github.com/huggingface/pytorch-image-models), [Ultralytics](https://github.com/ultralytics/ultralytics), [SuperGradients](https://github.com/Deci-AI/super-gradients), [RT-DETR](https://github.com/lyuwenyu/RT-DETR), and [YOLOv12](https://github.com/sunsmarterjie/YOLOv12).
- Train [custom models](#custom-models) with ease
- No self-supervised learning expertise required
- Automatic SSL method selection (coming soon!)
- Python, Command Line, and Docker support
- Built for [high performance](#performance) including [Multi-GPU](#multi-gpu) and [multi-node](#multi-node) support
- {ref}`Export models <export>` for fine-tuning or inference
- Generate and export {ref}`image embeddings <embed>`
- [Monitor training progress](#logging) with TensorBoard, Weights & Biases, and more

### Supported Models

[**Torchvision**](#torchvision)

- ResNet
- ConvNext

[**TIMM**](#timm)

- All models

[**Ultralytics**](#ultralytics)

- YOLOv5
- YOLOv6
- YOLOv8
- YOLO11
- YOLO12

[**RT-DETR**](#models-rtdetr)

- RT-DETR

[**YOLOv12**](#models-yolov12)

- YOLOv12

[**SuperGradients**](#super-gradients)

- PP-LiteSeg
- SSD
- YOLO-NAS

See [supported models](#models-supported-libraries) for a detailed list of all supported
models.

[Contact](#contact) us if you need support for additional models or libraries.

### Supported SSL Methods

- DINO
- DenseCL (experimental)
- SimCLR

See [methods](#methods) for details.

```{toctree}
---
hidden:
maxdepth: 2
---
quick_start
installation
train
export
embed
models/index
methods/index
performance/index
docker
tutorials/index
python_api/index
changelog
```

## License

Lightly**Train** is available under an AGPL-3.0 and a commercial license. Please contact us
at [info@lightly.ai](mailto:info@lightly.ai) for more information.

## Contact

[**Email**](mailto:info@lightly.ai) | [**Website**](https://www.lightly.ai/lightlytrain) | [**Discord**](https://discord.gg/xvNJW94)
