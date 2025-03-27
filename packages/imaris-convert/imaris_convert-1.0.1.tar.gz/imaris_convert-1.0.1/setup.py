from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imaris-convert",
    version="1.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "imaris_convert": [
            "*.dll",
            "*.py",
            "*.so",
            "*.dylib",
            "*.*"
        ],
    },
    install_requires=[
        "numpy",
        "tifffile",
        "tqdm",
    ],
    entry_points={
        'console_scripts': [
            'imaris-convert=imaris_convert.imaris_convert:main_cli',
        ],
    },
    author="Guanhao Sun",
    author_email="sgh4132@outlook.com",
    description="A tool for converting images to Imaris format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
)