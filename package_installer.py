import os

package = input('What package would you like to install?')

project_name = os.path.basename(os.getcwd())

command = 'D:/dom/Anaconda/envs/' + project_name + '/Scripts/pip install ' + package
print(command)
os.system(command)