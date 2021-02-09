import os
import git
import time

print("""

`7MMM.     ,MMF'      db            db       .M'''bgd 
  MMMb    dPMM       ;MM:          ;MM:     ,MI    "Y 
  M YM   ,M MM      ,V^MM.        ,V^MM.    `MMb.     
  M  Mb  M' MM     ,M  `MM       ,M  `MM      `YMMNq. 
  M  YM.P'  MM     AbmmmqMA      AbmmmqMA   .     `MM 
  M  `YM'   MM    A'     VML    A'     VML  Mb     dM 
.JML. `'  .JMML..AMA.   .AMMA..AMA.   .AMMA.P"Ybmmd"  

--- M E T A - A N A L Y S I S    A S S I S T A N T ---

""")

git_folder = os.getcwd()

print(f'\nLocated project folder: {git_folder}')
print(f'Pulling updates...\n')

g = git.cmd.Git(git_folder)
g.pull()

print(f'\nUpdate completed!\nThank you!.\n')
time.sleep(3)
