from setuptools import setup, find_packages

setup(
    name="tabulargrpo",  # Package name
    version="0.1.0",    # Version
    author="Dr. Enkhtogtokh",
    author_email="enkhtogtokh.java@gmail.com",
    description="A tabular GRPO classifier package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/enkhtogtokh/tabulargrpo",  # GitHub link
    packages=find_packages(),
    install_requires=[  # Dependencies
        "numpy",
        "pandas",
        "torch",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum Python version
)
