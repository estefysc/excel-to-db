import os

# os.walk is more efficient than os.dirlist
def search_for_file(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return True
    return False    

