# oa_pmc_extr

This repository automatically requests and extracts Full Text from Open Access PMC.

## Installation
oa_pmc_extr has a number of dependencies on other Python packages, it is recommended to install it in an isolated environment.

`git clone https://github.com/biomedicalinformaticsgroup/oa_pmc_extr.git`

`pip install ./oa_pmc_extr`

## Get started

The only function available in this repository is called 'pmc_oa_generation'. It only takes one argument 'PATH', which is the directory you want to save the output in. It has the default value './' meaning the current directory.

```python
from oa_pmc_extr import pmc_oa_generation
pmc_oa_generation(PATH)
```

## The result
