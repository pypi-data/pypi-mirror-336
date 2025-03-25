from setuptools import setup, find_packages

long_description = ""
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="splinetorch",
    version="0.0.1",
    description="SplineTorch is a Python package for fitting splines in PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    url="https://github.com/joakimwallmark/splinetorch",
    author="Joakim Wallmark",
    author_email="wallmark.joakim@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "torch>=2.1.1,<4.0.0",
        "numpy>=1.24.1,<3.0.0",
        "pandas>=2.2.0,<4.0.0",
        "matplotlib>=3.8.0,<5.0.0",
    ],
    zip_safe=False,
)
