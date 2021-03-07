#!/usr/bin/env python

"""
MAAS | Meta-analysis assistant DATA REFRESHER

This module updates dataset version to the latest version available at S3 bucket.
"""

import os
import time
import glob
from pathlib import Path

import git
import requests
from tqdm import tqdm


__author__ = "Aleksander Molak"
__copyright__ = "(C) 2021, Aleksander Molak"
__credits__ = ["Aleksander Molak"]
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Alekssander Molak"
__email__ = "aleksander.molak@gmail.com"
__status__ = "beta"

print(f"""

--------------- W E L C O M E  T O ------------------

`7MMM.     ,MMF'      db            db       .M'''bgd 
  MMMb    dPMM       ;MM:          ;MM:     ,MI    "Y 
  M YM   ,M MM      ,V^MM.        ,V^MM.    `MMb.     
  M  Mb  M' MM     ,M  `MM       ,M  `MM      `YMMNq. 
  M  YM.P'  MM     AbmmmqMA      AbmmmqMA   .     `MM 
  M  `YM'   MM    A'     VML    A'     VML  Mb     dM 
.JML. `'  .JMML..AMA.   .AMMA..AMA.   .AMMA.P"Ybmmd"  

--- M E T A - A N A L Y S I S   A S S I S T A N T ---

Current version (update module): {__version__} {__status__}
Contact: {__email__}

""")

with open(r'./app-data/data.dat', 'r') as f:
    DATA_PATH = f.readline()

with open(r'./app-data/s3.dat', 'r') as f:
    S3_URI = f.readline()

FILENAME = os.path.split(DATA_PATH)[1]
URI = fr'{S3_URI}/{FILENAME}'

data_file = Path(DATA_PATH)

if data_file.exists():

  print('\nYour data file seems up to date :)\n')

else:

  print(f'Downloading data from {URI}...\n')

  # Get stream
  response = requests.get(URI, stream=True)

  # Get metadata
  total_size_in_bytes = int(response.headers.get('content-length', 0))
  block_size = 1024 

  # Initialize progress bar
  progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

  with open(DATA_PATH, 'wb') as file:
      for data in response.iter_content(block_size):
          progress_bar.update(len(data))
          file.write(data)
  progress_bar.close()

  if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
      print("\nError :(")
  else:
      print('\nDone! :)')
  

print(f'\nUpdate completed!\n')
time.sleep(3)
