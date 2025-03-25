from setuptools import setup, find_packages

setup(
    name="retroPym",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[],
    author="---",
    author_email="retropy@respawnin.com",
    description="retroPy - a MicroPython retro game engine for the RP2350 micro-controller",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.retropy.io/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)