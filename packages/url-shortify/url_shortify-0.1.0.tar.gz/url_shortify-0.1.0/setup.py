from setuptools import setup, find_packages

setup(
    name="url_shortify",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "hashids>=1.3.1",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple URL shortener library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/url_shortify",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)