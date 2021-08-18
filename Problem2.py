import os


def find_files(suffix, path):
    """
    Find all files beneath path with file name suffix.

    Note that a path may contain further subdirectories
    and those subdirectories may also contain further subdirectories.

    There are no limit to the depth of the subdirectories can be.

    Args:
      suffix(str): suffix if the file name to be found
      path(str): path of the file system

    Returns:
       a list of paths
    """
    if not os.path.isdir(path):
        return "Path does not exist."

    def find_files_recursive(suffix, path):
        files = list()

        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            if item.endswith(suffix):
                files.append(item)

            if os.path.isdir(item_path):
                files.extend(find_files_recursive(suffix, item_path))

        return files

    files = find_files_recursive(suffix, path)

    if len(files) == 0:
        return "There were no files of the specified type in this directory " \
               "or any of the contained subdirectories."

    return files


print(find_files('.c', '../testdir/'))
# expected : ['b.c', 't1.c', 'a.c', 'a.c']
print(find_files('.c', './fake/'))
# expected : "Path does not exist."
print(find_files('.h', '../testdir/'))
# expected : ['b.h', 'a.h', 't1.h', 'a.h']
print(find_files('.cpp', '../testdir/'))
# expected : "There were no files of the specified type in this directory
#               or any of the contained subdirectories."
