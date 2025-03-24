from setuptools import setup, find_packages

setup(
    name="audio-mixer-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pydub"],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Python library to mix MP3 audio files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/audio-mixer-lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
