import os

def rename(file_name):
    return file_name[0]+prefix+file_name[1:]

def add_prefix_to_files_and_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Rename files
        # for filename in filenames:
        #     old_path = os.path.join(dirpath, filename)
        #     new_path = os.path.join(dirpath, rename(filename))
        #     print(new_path, old_path)
        #     os.rename(old_path, new_path)

        # # Rename directories
        for dirname in dirnames:
        #     old_path = os.path.join(dirpath, dirname)
        #     new_path = os.path.join(dirpath, rename(dirname))
        #     print (new_path, old_path)
        #     os.rename(old_path, new_path)
            filenames = os.listdir(os.path.join(dirpath, dirname))
            for filename in filenames:
                old_path = os.path.join(dirpath, dirname, filename)
                new_path = os.path.join(dirpath, dirname, rename(filename))
                print(new_path, old_path)
                os.rename(old_path, new_path)

        # Update dirnames to reflect the renamed directories
        dirnames[:] = [dirname for dirname in dirnames]

# Example usage
root_directory = "./SegmentedData/InputImages"
prefix = '00'
add_prefix_to_files_and_directories(root_directory)