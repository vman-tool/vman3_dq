from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vman3_dq",
    version="0.1.0",
    author="Isaac Lyatuu",
    author_email="ilyatuu@gmail.com",
    description="VMan3 Data Quality Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vman-tool/vman3-dq",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'chardet>=3.0.4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        'vman3_dq': ['data/*.csv'],
    },
)