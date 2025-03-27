from setuptools import setup
from setuptools_rust import RustExtension, Binding
import os

# Get the absolute path to the Rust core's Cargo.toml
core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core', 'Cargo.toml'))

setup(
    name="finatic-client-python",
    version="0.1.0",
    packages=["finatic"],
    package_dir={"": "src"},
    rust_extensions=[
        RustExtension(
            "finatic._core",
            binding=Binding.PyO3,
            path=core_path,
            features=["python"],
            py_limited_api=True,
        )
    ],
    zip_safe=False,
    python_requires=">=3.8",
    setup_requires=["setuptools-rust>=1.5.2"],
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
    },
) 