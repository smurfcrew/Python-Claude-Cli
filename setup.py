from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

requirements = (this_directory  / "requirements.txt").read_text().splitlines()

setup(
    name="claude-cli",
    version="1.0.0",
    author="Chris Padilla",
    author_email="chrispadilla110@gmail.com",
    description="A command-line interface for interacting with Claude AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smurfcrew/Python-Claude-Cli",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approvied :: MIT License"
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts":[
            "claude-cli=cli:main",
        ],
    },
    keywords="claude ai cli chatbot anthropic",
    project_urls={
        "Bug Reports":"https://github.com/smurfcrew/Python-Claude/issues",
        "Source" : "https://github.com/smurfcrew/Python-Claude-Cli",
    },
)