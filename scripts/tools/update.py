#!/usr/bin/env python

"""
MAAS | Meta-analysis assistant UPDATER

This module updates the MAAS version to the latest version available at github.
"""

import os
import git
import time


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


git_folder = os.getcwd()

print(f'\nLocated project folder: {git_folder}')
print(f'Pulling updates...\n')

g = git.cmd.Git(git_folder)
g.pull()

print(f'\nUpdate completed!\nThank you!.\n')
time.sleep(3)
