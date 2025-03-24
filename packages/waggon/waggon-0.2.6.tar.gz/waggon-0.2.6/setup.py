from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="waggon",
    version="0.2.6",
    description="WAsserstein Global Gradient-free OptimisatioN (WAGGON) methods library.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hse-cs/waggon",
    author="Tigran Ramazyan",
    author_email="ramazyant@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=["gpytorch==1.10.0", "matplotlib==3.7.5", "numpy==1.26.0",
                      "scikit_learn==1.3.2", "scipy==1.12.0", "setuptools==72.1.0",
                      "torch==2.2.2", "torchbnn==1.2", "torchensemble==0.1.9", "tqdm==4.66.4", "jax==0.4.38", "protes==0.3.11"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.11",
)
