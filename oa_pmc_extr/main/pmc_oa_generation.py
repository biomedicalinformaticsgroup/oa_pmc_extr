import os
import re
import shutil
import unicodedata
import time
import datetime
import wget 
import gzip
from bs4 import BeautifulSoup

def pmc_oa_generation(path = './'): 
    