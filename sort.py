from os import listdir, rename, rmdir
from pathlib import Path
import shutil
from sys import argv


# python3 sort.py '/home/mykhailo/Стільниця/dir_hlam' for test
PATH = argv[1]
list_type_r = set()
list_type_files = dict(zip(['images', 'video', 'archives', 'documents', 'audio'],
                           [set(), set(), set(), set(), set()]))
dict_arrange = dict(zip(['images', 'video', 'archives', 'documents', 'audio'],
                            [('JPEG', 'PNG', 'JPG', 'SVG'),
                             ('AVI', 'MP4', 'MOV', 'MKV'), ('ZIP', 'GZ', 'TAR'),
                             ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
                             ('MP3', 'OGG', 'WAV', 'AMR')
                             ]))
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k",
               "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts",
               "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i",
               "ji", "g")
all_known_type = ['JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV',
                 'ZIP', 'GZ', 'TAR', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX',
                 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR']
all_unknown_type = set()

def arrange_dir(dir):
    val = listdir(dir)
    p = Path(dir)
    for i in dict_arrange:
        (p / i).mkdir()
    for file_name in val:
        q = p / file_name
        if q.is_dir():
            arrange_dir(q)
        else:
            list_type_r.add(file_name.split('.')[-1])
            for dir_in, type_f in dict_arrange.items():
                if file_name.split('.')[-1].upper() not in all_known_type:
                    all_unknown_type.add(file_name.split('.')[-1])
                if file_name.split('.')[-1].upper() not in type_f:
                    continue
                list_type_files[dir_in].add(str(file_name))
                if file_name.split('.')[-1].upper() in dict_arrange['archives']:
                    unzip(q, p / dir_in / file_name.split('.')[0])
                    break
                else:
                    shutil.move(str(dir) + '/' + file_name,
                                str(PATH) + '/' + dir_in)
                    break
    check_name(dir)
    del_empy_dir(dir)


def unzip(file, dir):
    shutil.unpack_archive(file, dir)
    file.unlink()


def check_name(dir):
    val = listdir(dir)
    for k in val:
        l = Path(dir)
        p = l / k
        if p.is_dir():
            val2 = listdir(p)
            for i in val2:
                j = normalize(i)
                if j != i:
                    rename(p / i, p / j)


def normalize(file_name: str):
    def translate(name):
        trans = {}
        for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            trans[ord(c)] = l
            trans[ord(c.upper())] = l.upper()
        return name.translate(trans)
    res = ''
    for i in file_name:
        if 96 < ord(i) < 123 or 64 < ord(i) < 91 or i.isdigit() or i == '.':
            res += i
        elif 1039 < ord(i) < 1104:
            res += translate(i)
        else:
            res += '_'
    return res


def del_empy_dir(dir):
    val = listdir(dir)
    p = Path(dir)
    for i in val:
        if (p / i).is_dir():
            try:
                rmdir(p / i)
            except OSError:
                pass


if __name__ == '__main__':
    arrange_dir(PATH)
    string_return = ''
    string_return += 'Список файлів в кожній категорії ' \
                     '(музика, відео, фото и ін.)\n\n'
    for i, j in list_type_files.items():
        string_return += i + ' :' + str(j) + '\n'
    string_return += f'\nПерелік усіх відомих скрипту розширень,' \
                     f' які зустрічаються в цільовій папці: {list_type_r}'
    string_return += f'\nПерелік всіх розширень, які скрипту невідомі:' \
                     f' {all_unknown_type}'
    print(string_return)
