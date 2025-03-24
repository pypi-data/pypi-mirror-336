from setuptools import setup, find_packages

setup(
    name="bilibili-search-cli",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line tool to search videos on Bilibili",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bilibili-search-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "fake-useragent>=0.1.11",
    ],
    entry_points={
        "console_scripts": [
            "bilibili-search=bilibili_search_cli.cli:main",
        ],
    },
) 