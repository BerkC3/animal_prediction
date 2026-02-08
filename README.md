# 🦁 Animal Classification AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-87.38%25-brightgreen.svg)

**Deep learning-powered animal image classifier with a modern web interface**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Model](#-model-information)

</div>

---

## 📖 Overview

This project is an AI-powered animal image classification system that can identify **50 different animal species** with **87.38% accuracy**. Built with PyTorch and served through a beautiful Gradio web interface.

## ✨ Features

- 🎯 **High Accuracy**: ResNet18 model trained to 87.38% accuracy
- 🖼️ **Easy to Use**: Drag-and-drop image upload
- 🌙 **Modern UI**: Beautiful dark-themed Gradio interface
- ⚡ **GPU Support**: Automatic CUDA detection for faster inference
- 📊 **Top-5 Predictions**: Shows confidence scores for top predictions
- 🔌 **API Ready**: Built-in REST API endpoint

## 🎬 Demo

<div align="center">

| Upload Image | Get Predictions |
|:---:|:---:|
| Drag & drop or click to upload | View top-5 predictions with confidence |

</div>

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) NVIDIA GPU with CUDA for faster inference

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/animal-classification-ai.git
cd animal-classification-ai
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Model File

> ⚠️ **Note**: The trained model file (`ResNet18_Animals_Best_Acc87.38.pth`) is **not included** in this repository.
> 
> This is a portfolio project demonstrating my deep learning and software development skills. If you want to train your own model, you can use the [Animals-50 dataset](https://www.kaggle.com/datasets) with a ResNet18 architecture.

## 🚀 Usage

### Option 1: Web Interface (Recommended)

```bash
python app.py
```

Open your browser at `http://localhost:7860`

### Option 2: Windows Batch File

Double-click `run_app.bat` to start the application automatically.

### Option 3: Python API

```python
from backend import Predictor
from PIL import Image

# Initialize predictor
predictor = Predictor("ResNet18_Animals_Best_Acc87.38.pth")

# Load and classify image
image = Image.open("your_animal_image.jpg")
predictions = predictor.get_top_predictions(image, top_k=5)

print(predictions)
# Output: {'lion': 0.85, 'tiger': 0.08, 'leopard': 0.03, ...}
```

## 🦊 Supported Animals

The model can classify the following **50 animal species**:

<details>
<summary>Click to expand full list</summary>

| | | | | |
|---|---|---|---|---|
| Antelope | Bat | Beaver | Blue Whale | Bobcat |
| Buffalo | Chihuahua | Chimpanzee | Collie | Cow |
| Dalmatian | Deer | Dolphin | Elephant | Fox |
| German Shepherd | Giant Panda | Giraffe | Gorilla | Grizzly Bear |
| Hamster | Hippopotamus | Horse | Humpback Whale | Killer Whale |
| Leopard | Lion | Mole | Moose | Mouse |
| Otter | Ox | Persian Cat | Pig | Polar Bear |
| Rabbit | Raccoon | Rat | Rhinoceros | Seal |
| Sheep | Siamese Cat | Skunk | Spider Monkey | Squirrel |
| Tiger | Walrus | Weasel | Wolf | Zebra |

</details>

## 🔬 Model Information

| Property | Value |
|----------|-------|
| **Architecture** | ResNet18 |
| **Framework** | PyTorch |
| **Input Size** | 224 × 224 |
| **Classes** | 50 |
| **Accuracy** | 87.38% |
| **Normalization** | ImageNet standards |

### Performance

| Device | Inference Time |
|--------|----------------|
| CPU | ~2-5 seconds |
| GPU (CUDA) | ~0.1-0.5 seconds |

## 📁 Project Structure

```
animal-classification-ai/
├── 📄 app.py                  # Gradio web interface
├── 📄 backend.py              # Model loading & prediction logic
├── 📄 requirements.txt        # Python dependencies
├── 📄 run_app.bat             # Windows launcher script
├── 📄 README.md               # Project documentation
└── 📄 .gitignore              # Git ignore rules
```

> 💡 **Note**: Model weights (`.pth`) are not included. See [Installation](#step-4-model-file) for details.

## ⚙️ Configuration

### Change Port

Edit `app.py`:

```python
interface.launch(
    server_port=8080,  # Change to your preferred port
)
```

### Enable Public Sharing

```python
interface.launch(
    share=True,  # Creates a public URL
)
```

## 🐛 Troubleshooting

<details>
<summary><b>Model file not found</b></summary>

The model file is not included in this repository. You need to train your own model using a ResNet18 architecture on an animal dataset.
</details>

<details>
<summary><b>CUDA not available</b></summary>

This is normal if you don't have an NVIDIA GPU. The app will use CPU mode automatically.
</details>

<details>
<summary><b>Slow performance on CPU</b></summary>

CPU inference takes 2-5 seconds per image. For faster results, use a CUDA-enabled GPU.
</details>

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ResNet architecture by Microsoft Research
- Gradio for the amazing UI framework
- PyTorch team for the deep learning framework

---

<div align="center">

**⭐ Star this repo if you found it useful!**

Made with ❤️ and PyTorch

</div>
