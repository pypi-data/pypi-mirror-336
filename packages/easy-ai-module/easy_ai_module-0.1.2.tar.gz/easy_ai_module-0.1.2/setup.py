from setuptools import setup, find_packages

setup(
    name="easy_ai_module",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    description="A simple module for making AI requests to Gemini API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="You",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/easy_ai_module",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 