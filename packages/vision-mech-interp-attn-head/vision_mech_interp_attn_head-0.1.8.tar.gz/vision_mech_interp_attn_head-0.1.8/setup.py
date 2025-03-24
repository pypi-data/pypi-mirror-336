from setuptools import setup, find_packages

setup(
    name="vision_mech_interp_attn_head",
    version="0.1.8",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "transformers",
        "peft",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "Pillow",
    ],
    description="A package for vision mechanistic interpretability",
    author="Nooshin Bahador",
    author_email="nooshin.bah@gmail.com",
    url="https://github.com/nbahador/vision_mech_interp_attn_head",
)