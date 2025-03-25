# **OPTIMA35**
**OPTIMA35** stands for **Organizing, Processing, Tweaking Images, and Modifying Analogs from 35mm Film**. It is a Python package designed to simplify image editing and metadata management, providing an interface/API for handling image and EXIF data seamlessly. While OPTIMA35 was created with analog photography in mind—where scanned images often lack proper EXIF data or retain only scanner metadata—it is equally useful for digital images. Adding or managing EXIF data is invaluable for organizing private photo collections, making your photo library more structured and searchable.

OPTIMA35 is a core package that acts as an interface for libraries like Pillow and piexif, simplifying image manipulation tasks. While it modifies images one at a time, it requires a dedicated program for flexible and batch processing. For a user-friendly graphical experience, consider using [OptimaLab35](https://gitlab.com/CodeByMrFinchum/OptimaLab35), a GUI designed specifically for OPTIMA35, also developed by me.

Currently, there are no plans to create a formal API documentation. The code includes annotations and detailed function descriptions to explain its functionality. As this is a private hobby project, dedicating time to writing comprehensive documentation would take away from my limited free time.

---

## **Features**

### **Image Processing**
- Resize images (upscale or downscale)
- Convert images to grayscale
- Adjust brightness and contrast
- Add customizable text-based watermarks

### **EXIF Management**
- Add EXIF data using a simple dictionary
- Copy EXIF data from the original image
- Remove EXIF metadata completely
- Add timestamps (e.g., original photo timestamp)
- Automatically adjust EXIF timestamps based on image file names
- Add GPS coordinates to images

### **Streamlined Integration**
- Handles all required EXIF byte conversions behind the scenes
- Provides an intuitive API for frequently needed operations

---

## **Installation**
Install the GUI (dependencies are installed automatically)
```bash
pip install OptimaLab35
```

Or in case you only want optima35 (dependencies are installed automatically):
```bash
pip install optima35
```

---

## **Current Status**
**Stable Release (v1.0)**
- The program follows semantic versioning (**major.minor.patch**).
- The current release is stable, and all changes within the same major version will remain backward compatible.
- Breaking changes, if any, will result in a new major version.
- Future development will primarily focus on the graphical user interface (OptimaLab35), with only minor updates or patches for OPTIMA35 as needed.

---
# Contribution

Thanks to developer [Mr Finch](https://gitlab.com/MrFinchMkV) for contributing to this project, and for initiating and helping setting up the CI/CD pipeline.

## Use of LLMs
In the interest of transparency, I disclose that Generative AI (GAI) large language models (LLMs), including OpenAI’s ChatGPT and Ollama models (e.g., OpenCoder and Qwen2.5-coder), have been used to assist in this project.

### Areas of Assistance:
- Project discussions and planning
- Spelling and grammar corrections
- Suggestions for suitable packages and libraries
- Guidance on code structure and organization

In cases where LLMs contribute directly to code or provide substantial optimizations, such contributions will be disclosed and documented in the relevant sections of the codebase.

**Ollama**
- mradermacher gguf Q4K-M Instruct version of infly/OpenCoder-1.5B
- unsloth gguf Q4K_M Instruct version of both Qwen/QWEN2 1.5B and 3B

#### References
1. **Huang, Siming, et al.**
   *OpenCoder: The Open Cookbook for Top-Tier Code Large Language Models.*
   2024. [PDF](https://arxiv.org/pdf/2411.04905)

2. **Hui, Binyuan, et al.**
   *Qwen2.5-Coder Technical Report.*
   *arXiv preprint arXiv:2409.12186*, 2024. [arXiv](https://arxiv.org/abs/2409.12186)

3. **Yang, An, et al.**
   *Qwen2 Technical Report.*
   *arXiv preprint arXiv:2407.10671*, 2024. [arXiv](https://arxiv.org/abs/2407.10671)
