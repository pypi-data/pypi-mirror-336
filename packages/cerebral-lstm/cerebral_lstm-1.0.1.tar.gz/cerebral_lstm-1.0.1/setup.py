from setuptools import setup, find_packages

# Read the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cerebral_lstm",
    version="1.0.1",  # Update this version number for new releases
    author="Ravin Kumar",
    author_email="mr.ravin_kumar@hotmail.com",  # Replace with your email
    description="A PyTorch implementation of Cerebral LSTM: A Better Alternative for Single- and Multi-Stacked LSTM Cell-Based RNNs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-ravin/cerebral_lstm",  # Link to your GitHub repository
    project_urls={
        "Bug Tracker": "https://github.com/mr-ravin/cerebral_lstm/issues",  # Link to issues page
        "Documentation": "https://github.com/mr-ravin/cerebral_lstm#readme",  # Link to documentation
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),  # Automatically find packages in the directory
    python_requires=">=3.7",  # Minimum Python version required
    install_requires=[
        "torch>=1.10.0",  # PyTorch is the only dependency
    ],
    keywords=[
        "deep learning",
        "lstm",
        "recurrent neural networks",
        "pytorch",
        "sequence modeling",
        "cerebral lstm",
        "rnn",
    ],
    license="MIT",  # License type
)
