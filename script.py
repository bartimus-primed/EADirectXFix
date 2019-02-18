#!python
from os import path, listdir, remove, popen
import subprocess


# Launch the installer
def launch_installer(direct_x_path):
    try:
        full_qual_name = path.join(direct_x_path, "DXSETUP.exe /silent")
        out = subprocess.run("DXSETUP.exe /silent", shell=True, check=True, capture_output=True, cwd=direct_x_path)
        if out.returncode == 0:
            print("Successfully installed directx in {}".format(full_qual_name))
    except:
        print("Failed to install directX in {}".format(full_qual_name))


# Delete the files
def delete_files(direct_x_path):
    # The meat and potatoes of the script, check if our files match our list of ok'd prefixes
    white_list = [".exe", ".dll", "2010"]
    for f in listdir(direct_x_path):
        # Using pythons list comprehension, check if any file is not in the whitelist
        if not any(white_listed in f for white_listed in white_list):
            print("Removing : {}".format(f))
            remove(path.join(direct_x_path, f))
        # We don't need these else's but I put them there so the code is more verbose
        else:
            continue

# Check if the directx directory exists
def check_for_directx_dir(installer_directory):
    for folder in listdir(installer_directory):
        # Check if the folder is named directx
        if folder == "directx":
            # Send the directx folder to delete files
            delete_files(path.join(installer_directory, folder, "redist"))
            # Launch the installer
            launch_installer(path.join(installer_directory, folder, "redist"))
        # We don't need these else's but I put them there so the code is more verbose
        else:
            continue

# List all folders in the origin game directory
def get_folders(path_name):
    # Get the game folders
    folders = listdir(path_name)
    for dirs in folders:
        # Check each game folder
        directory = listdir(path.join(path_name, dirs))
        for folder in directory:
            # If the game folder has an __Installer directory, send it to check if directx is in there.
            if folder == "__Installer":
                check_for_directx_dir(path.join(path_name, dirs, folder))
            # We don't need these else's but I put them there so the code is more verbose
            else:
                continue

if __name__ == "__main__":
    directx_path = 'C:\Program Files (x86)\Origin Games'
    get_folders(directx_path)
