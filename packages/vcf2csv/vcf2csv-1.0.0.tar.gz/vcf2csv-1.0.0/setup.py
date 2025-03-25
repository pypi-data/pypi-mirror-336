from setuptools import setup, find_packages

setup(
    name="vcf2csv",
    version="1.0.0",
    description="VCARD 3.0 to CSV Converter with Apple Extensions",
    author="jrkoop",
    packages=find_packages(),
    py_modules=["vcf_parser"],
    entry_points={
        "console_scripts": [
            "vcf2csv=vcf_parser:main"
        ]
    },
    install_requires=[
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)