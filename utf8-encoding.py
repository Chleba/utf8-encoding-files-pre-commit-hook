import os
import codecs
import glob
import chardet

CHUNK_SIZE = 4096;
ROOT_DIR = './test/';
ALL_FILES = [];

CPP_FILES = glob.iglob(ROOT_DIR + '**/*.cpp', recursive=True);
HEADER_FILES = glob.iglob(ROOT_DIR + '**/*.hpp', recursive=True);

ALL_FILES = list(CPP_FILES) + list(HEADER_FILES);

def files_encoding_function():
    """Check encoding and convert to UTF-8, if encoding is not UTF-8."""
    print(".. get all *.c, *.cpp, *.h, *.hpp files from root ..");
    for filename in ALL_FILES:
        #  Not 100% accuracy:
        #  https://stackoverflow.com/a/436299/5951529
        #  Check:
        #  https://chardet.readthedocs.io/en/latest/usage.html#example-using-the-detect-function
        #  https://stackoverflow.com/a/37531241/5951529
        with open(filename, 'rb') as opened_file:
            bytes_file = opened_file.read();
            chardet_data = chardet.detect(bytes_file);
            fileencoding = (chardet_data['encoding']);

            if fileencoding != None:
                if fileencoding in ['ascii', 'utf-8']:
                    print(filename + ' in UTF-8 encoding')
                else:
                    with codecs.open(filename, 'r', fileencoding) as file_for_conversion:
                        with codecs.open(filename + '_new', 'w', 'utf-8') as converted_file:
                            while True:
                                content = file_for_conversion.read(CHUNK_SIZE);
                                if not content:
                                    break;
                                converted_file.write(content);

                    # rename converted file and remove old one
                    os.remove(filename);
                    os.rename(filename + '_new', filename);

                    print(filename +
                        ' in ' +
                        fileencoding +
                        ' encoding automatically converted to UTF-8');
        
def main() -> int:
    files_encoding_function();
    return 0;

if __name__ == '__main__':
    exit(main());

