from setuptools import setup, find_packages

setup(
    name="rossini",
    version="2.0.0",
    author="#asytric",
    author_email="eusmool@gmail.com",
    description="Next-Gen Multimodal Audio-Visual Generation Framework",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "torch>=2.1.0",
        "torchaudio>=2.1.0",
        "torchvision>=0.16.0",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "pillow>=10.0.0",
        "pydantic>=2.5.0",
        "requests>=2.31.0",
        "soundfile>=0.12.1",
        "diffusers>=0.25.0",
        "transformers>=4.36.0",
        "accelerate>=0.25.0",
    ],
    entry_points={
        "console_scripts": [
            "rossini=rossini.cli:main",
        ],
    },
)