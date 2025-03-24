from setuptools import setup, find_packages

setup(
    name="mytorch123",
    version="0.3.1",
    description="Drop-in replacement for PyTorch that does distributed training and inference on a remote server",
    long_description=open('../README.md').read(),  # Note: path changed
    long_description_content_type='text/markdown',
    author="mytorch.net",
    author_email='pypi@mytorch.net',
    url="https://mytorch.net",
    classifiers=[
       "Development Status :: 4 - Beta",
       "Intended Audience :: Developers",
       "Intended Audience :: Science/Research",
       "Programming Language :: Python :: 3.10",
       "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "grpcio>=1.65.0",
        "grpcio-tools>=1.65.0",
        "numpy",
        "requests",
        "pillow",
        "tqdm",
        "matplotlib",
        "scikit-learn",
        "huggingface-hub"
    ],
    py_modules=["MyTorchClient"],
    packages=find_packages(
        include=[
            "torch*",
            "transformers*",
            "torchvision*",
            "proxies*", 
            "gRPC_impl*",
            "utils*",
            "connection_utils*",
        ],
        exclude=[
            "venv*",
            "venv.*",
            "*.venv*"
        ]
    ),
    package_data={
        'torch': ['*.py'],
        'transformers': ['*.py'],
        'torchvision': ['*.py'],
        'proxies': ['*.py'],
        'gRPC_impl': ['*.py'],
        'utils': ['*.py'],
        'connection_utils': ['*.py'],
    },
) 
