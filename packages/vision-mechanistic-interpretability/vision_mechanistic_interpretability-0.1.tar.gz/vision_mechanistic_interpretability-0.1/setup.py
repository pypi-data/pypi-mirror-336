from setuptools import setup, find_packages

setup(
    name="vision_mechanistic_interpretability",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "transformers",
        "peft",
        "matplotlib",
        "seaborn",
        "pandas",
        "numpy",
        "Pillow",
    ],
    description="A package for mechanistic interpretability of vision models.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/vision_mechanistic_interpretability",
)