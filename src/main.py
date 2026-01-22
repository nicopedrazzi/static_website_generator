from textnode import TextNode, TextType
import logging
import os
import shutil

def from_source_to_dest(source_path, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    for entry in os.listdir(dest_path):
        entry_path = os.path.join(dest_path, entry)
        if os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
        else:
            os.remove(entry_path)

    for entry in os.listdir(source_path):
        source_entry = os.path.join(source_path, entry)
        dest_entry = os.path.join(dest_path, entry)
        if os.path.isdir(source_entry):
            logging.info("Copying directory %s -> %s", source_entry, dest_entry)
            shutil.copytree(source_entry, dest_entry)
        else:
            logging.info("Copying file %s -> %s", source_entry, dest_entry)
            shutil.copy2(source_entry, dest_entry)



def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    from_source_to_dest("static/","public/")
    

if __name__ == "__main__":
    main()
