# oa_pmc_extr

This repository automatically requests and extracts Full Text from Open Access PMC for use in non-commercial research. 

## Installation
oa_pmc_extr has a number of dependencies on other Python packages, it is recommended to install it in an isolated environment.

`git clone https://github.com/biomedicalinformaticsgroup/oa_pmc_extr.git`

`pip install ./oa_pmc_extr`

After installation, you can remove the file if you want using:

`rm -rf oa_pmc_extr`

You can also uninstall oa_pmc_extr using:

`pip uninstall oa_pmc_extr`

## Get started

The only function available in this repository is called 'pmc_oa_generation'. It only takes one argument 'PATH', which is the directory you want to save the output in. It has the default value './' meaning the current directory.

```python
from oa_pmc_extr import pmc_oa_generation
pmc_oa_generation(PATH)
```

 The funtion is extracting the files from [/pub/pmc/oa_bulk](https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/) API using ftp requests from the oa_comm, oa_noncomm, and oa_other sets.

## The result
The function will generate a pre-made directory called ```pmc_oabulk_output```. Within ```pmc_oabulk_output``` there are three subdirectories called ```parsed_files```, ```unzip_files```, and ```zip_files```. All of the subdirectories contains 2 directories, ```txt``` and ```xml```. The files contained in these directories are obtained from the [PMC API](https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/) for all 3 licenses type (commercial, non commercial, and other). 
- ```zip_files``` contains the raw files obtained directly from the API. There are .gz files containing the PMC files in .txt or .xml, the filelists containing metadata about the PMC files saved as .txt and .csv. 
- ```unzip_files``` contains the uncompressed PMC files from the .gz files. These are saved in a pre-made directory made by PMC. They look like 'PMC000xxxxxx'.
- ```parsed_files``` contains the same structure as ```unzip_files``` but the file were loaded and clean to remove the information outside the full text.