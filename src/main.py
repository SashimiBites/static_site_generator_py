import os, shutil
from utils import copy_files_recursive, generate_pages_recursive


def main():
    dest_dir = "public"
    src_dir = "static"
    for filename in os.listdir(dest_dir):
        file_path = os.path.join(dest_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

    copy_files_recursive(src_dir, dest_dir)
    generate_pages_recursive("content", "template.html", "public")


main()
