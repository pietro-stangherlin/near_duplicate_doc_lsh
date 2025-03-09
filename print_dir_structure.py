import os

def list_files(startpath):
    '''
    Args:
        -param startpath (str): path of the main directory
    Print: 
        -the directory structure using startpah as root
    '''
    for root, dirs, files in os.walk(startpath):
        if '.git' in dirs:
            dirs.remove('.git')  # don't visit .git directories
        level = root.replace(startpath, '').count(os.sep)
        indent = '|   ' * (level - 1) + '|-- ' if level > 0 else ''
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = '|   ' * level + '|-- '
        for f in files:
            print('{}{}'.format(subindent, f))

if __name__ == "__main__":
    list_files(os.getcwd())

# how to use it to print the dir structure from the current directory as a root
# >>> python .\print_dir_structure.py > dir_structure.txt