from setuptools import setup, find_packages

setup(
    name="tesseractpro",
    version="0.1.4",
    description="The Tesseract Pro Python API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Emiel van Goor",
    author_email="info@tesseractpro.io",
    url="https://github.com/tesseractpro/python-api",
    packages=find_packages(include=["tesseractpro", "tesseractpro.*"]),
    install_requires=[
        "python-socketio[client]>=5.0.0",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    license="MIT",
    keywords="TesseractPro API",
)
