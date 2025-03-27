from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kdai-node-client",
    version="0.2.3",
    author="KDAI Team",
    author_email="support@kdai.io",
    description="Client library for connecting nodes to the KDAI distributed AI platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kdai-io/kdai-node-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "websocket-client>=1.2.0",
        "psutil>=5.8.0",
        "pydantic>=1.9.0",
        "tqdm>=4.62.0",
    ],
    entry_points={
        "console_scripts": [
            "kdai-node=kdai_node_client.cli:main",
        ],
    },
)
