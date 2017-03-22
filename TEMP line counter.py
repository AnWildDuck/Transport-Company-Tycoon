import os, time

while True:
        
    def list_files(dir):
        r = []
        for root, dirs, files in os.walk(dir):
            for name in files:
                r.append(os.path.join(root, name))
        return r

    print('What file should I search?')
    dir = input()

    # Get all files
    files = list_files(dir)

    # Get all python files
    python_files = []

    for file_name in files:
        if file_name[len(file_name) - 4:] == '.pyw' or file_name[len(file_name) - 3:] == '.py':
            if not 'TEMP' in file_name:
                python_files.append(file_name)

    # Get the length of each file
    length = 0

    for file_name in python_files:
        contents = open(file_name, 'r').read()
        lines = contents.splitlines()
        length += len(lines)


    # Show
    print(length, 'lines in', len(python_files), 'python files')
    print()
    
    time.sleep(1)
