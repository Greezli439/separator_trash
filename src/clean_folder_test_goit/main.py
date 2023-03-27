from os import listdir, rename, rmdir
from pathlib import Path
import shutil
from pprint import pprint

PATH = '/Users/mykhailo/Desktop/arrange_dir'


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k",
               "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts",
               "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i",
               "ji", "g")
FOR_TRANSLIT = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    FOR_TRANSLIT[ord(c)] = l
    FOR_TRANSLIT[ord(c.upper())] = l.upper()
TYPE_DIR = {
    'AMR': 'audio',
    'AVI': 'video',
    'DOC': 'documents',
    'DOCX': 'documents',
    'GZ': 'archives',
    'JPEG': 'images',
    'JPG': 'images',
    'MKV': 'video',
    'MOV': 'video',
    'MP3': 'audio',
    'MP4': 'video',
    'OGG': 'audio',
    'PDF': 'documents',
    'PNG': 'images',
    'PPTX': 'documents',
    'SVG': 'images',
    'TAR': 'archives',
    'TXT': 'documents',
    'WAV': 'audio',
    'XLSX': 'documents',
    'ZIP': 'archives'}


list_type_files = dict(zip(['images', 'video', 'archives', 'documents', 'audio', 'unknown'],
                           [set(), set(), set(), set(), set(), set()]))




def arrange_dir(path):
    path = Path(path)
    main(path, path)

def main(PATH, path):
    val = listdir(path)
    make_dir(path)
    for file_name in val:
        if (path_file_name := path / file_name).is_dir():
            main(PATH, path_file_name)
            continue
        dir_for_file = determine_file_type(file_name)
        if dir_for_file == 'archives':
            unpack(path_file_name, PATH / dir_for_file / file_name.split('.')[0])
        else:
            move_file(PATH, dir_for_file, path_file_name)
    del_empy_dir(path)

def del_empy_dir(path):
    val = listdir(path)
    for i in val:
        if (path / i).is_dir():
            try:
                rmdir(path / i)
            except OSError:
                pass
def move_file(PATH, dir_for_file, path_file_name):
    shutil.move(path_file_name, PATH / dir_for_file)

def unpack(path_file_name, dir):
    shutil.unpack_archive(path_file_name, dir)
    path_file_name.unlink()

def determine_file_type(file_name):
    try:
        dir_for_file = TYPE_DIR[file_name.split('.')[-1].upper()]
    except:
        dir_for_file = 'unknown'
    return dir_for_file



def make_dir(path):
    for name_dir in list_type_files:
        (path / name_dir).mkdir()

def normalize(file_name):
    res = ''
    for i in file_name:
        if 96 < ord(i) < 123 or 64 < ord(i) < 91 or i.isdigit() or i == '.':
            res += i
        elif 1039 < ord(i) < 1111:
            res += i.translate(FOR_TRANSLIT)
        else:
            res += '_'
    return res


if __name__ == '__main__':
    arrange_dir(PATH)




    # Замінює всі символи крім латинських літер, цифр на '_'.