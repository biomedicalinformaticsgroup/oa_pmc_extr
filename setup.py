import setuptools
   
setuptools.setup(
    name="oa_pmc_extr",
    version="0.1.0",
    author="Antoine Lain, Ian Simpson",
    author_email="Antoine.Lain@ed.ac.uk, Ian.Simpson@ed.ac.uk",
    description="This repository automatically requests and extracts Full Text from Open Access PMC for use in non-commercial research.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
'bs4',
'wget',
'python-dateutil',
'IPython',
'lxml',
],
    python_requires='>=3.6'
)