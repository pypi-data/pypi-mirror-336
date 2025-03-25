from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto-doc-utils",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automatic documentation utilities for Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/auto-doc-utils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'genreq=auto_doc_utils.requirements_generator:main',
            'analyze=auto_doc_utils.project_analyzer:main',
        ],
    },
    install_requires=[
        # Add dependencies here, if any
    ],
)