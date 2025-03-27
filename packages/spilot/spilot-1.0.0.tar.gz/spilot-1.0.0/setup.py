from setuptools import setup, find_packages

setup(
    name="spilot",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "spilot": ["style.css"],
    },
    entry_points={
        'console_scripts': [
            'spilot=spilot.cli:main',
        ],
    },
    install_requires=[
        "textual>=0.38.1",
    ],
    author="Saurabh Atreya",
    author_email="saurabh@atrey-a.com",
    description="A terminal-based SLURM job monitoring utility that provides a clean, interactive TUI for viewing and managing jobs on HPC clusters.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/atrey-a/spilot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)