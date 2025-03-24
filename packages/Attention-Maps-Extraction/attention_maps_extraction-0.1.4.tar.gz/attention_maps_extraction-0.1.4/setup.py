from setuptools import setup, find_packages

setup(
    name="Attention-Maps-Extraction",
    version="0.1.4",
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
    description="A package for extracting attention maps.",
    author="Nooshin Bahador",
    author_email="nooshin.bah@gmail.com",
    url="https://github.com/nbahador/Attention_Maps_Extraction",
)