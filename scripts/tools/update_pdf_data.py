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

import pandas as pd


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


#### DOWNLOAD PDF UPDATES FILE ####

URI = 'https://cbu-pdf.s3.us-east-2.amazonaws.com/data/PDF_UPDT_ONLY__2021-03-24_20-03-09.csv'

DATA_PATH = r'./data/PDF_UPDT_ONLY__2021-03-24_20-03-09.csv'

data_file = Path(DATA_PATH)

if data_file.exists():

  print('\nYour data file seems up to date :)\n')

else:
  os.makedirs('./data', exist_ok=True)
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
      print('\nDownload done.')
  


#### JOIN DFs ####

# Read-in the current data
with open(r'./app-data/data.dat', 'r') as f:
    ORIGINAL_DATA_PATH = f.readline()

# Read-in the files
data = pd.read_csv(ORIGINAL_DATA_PATH)
updates = pd.read_csv(DATA_PATH)

# Backup the original file
BACKUP_PATH = ORIGINAL_DATA_PATH[:-4] + '_backup.csv'

print('\nCreating backup copy...')
data.to_csv(BACKUP_PATH, index=False)


print('\nUpdating PDF information...\n')

for idx in tqdm(updates.IDrec):
    
    d = data[data.IDrec == idx].index.values[0]
    
    new_title = updates[updates.IDrec == idx].web_title.values[0]
    new_authors = updates[updates.IDrec == idx].web_authors.values[0]
    new_pdf_fn = updates[updates.IDrec == idx].pdf_dwnld_filename.values[0]
    new_pdf_dwnld = updates[updates.IDrec == idx].pdf_dowloaded.values[0]
    
    data.at[d, "web_title"] = new_title
    data.at[d, "web_authors"] = new_authors
    data.at[d, "pdf_dwnld_filename"] = new_pdf_fn
    data.at[d, "pdf_dowloaded"] = new_pdf_dwnld


# Store the updated file
print('\nStoring updates...')
data.to_csv(ORIGINAL_DATA_PATH, index=False)


print(f'\nUpdate completed!\n')
time.sleep(3)
