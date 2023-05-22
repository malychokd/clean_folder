import sys
import os
import shutil
from pathlib import Path

def get_group(this_suffix):
    if list_image.count(this_suffix) > 0:
        list_extensions.add(this_suffix)
        return 'images'
    if list_video.count(this_suffix) > 0:
        list_extensions.add(this_suffix)
        return 'video'
    if list_doc.count(this_suffix) > 0:
        list_extensions.add(this_suffix)
        return 'documents'
    if list_music.count(this_suffix) > 0:
        list_extensions.add(this_suffix)
        return 'audio'
    if list_zip.count(this_suffix) > 0:
        list_extensions.add(this_suffix)
        return 'archives'
    list_unknown_extensions.add(this_suffix)
    return 'other'    

def normalize(name_this_f):
    new_name = name_this_f.translate(TRANS)
    new_name2 = ''
    for i in new_name:
        tek_ord = ord(i)
        if tek_ord < 48 or (tek_ord > 57 and tek_ord < 65) or (tek_ord > 90 and tek_ord < 97) or tek_ord > 122:
            new_name2 += '_'
        else:
            new_name2 += i    
    return new_name2

def analysis_my_files(temp_folder):
    new_name = normalize(temp_folder.name)
    if new_name != temp_folder.name:
        temp_folder = Path(rename_my_files(temp_folder, new_name))

    for p_ob in temp_folder.iterdir():
        if p_ob.is_dir():
            analysis_my_files(p_ob)
        else:
            new_name = normalize(p_ob.name.rstrip(p_ob.suffix))
            if new_name != p_ob.name:
                rename_my_files(p_ob, new_name, p_ob.suffix)    

            this_suffix = p_ob.suffix.lstrip(".").upper()
            group = get_group(this_suffix)
            this_file = {'name': new_name+p_ob.suffix, 'parent': p_ob.parent, 'suffix': p_ob.suffix, 'group': group}
            list_file.append(this_file)

def rename_my_files(temp_folder, new_name, suffix=''):
    if temp_folder.is_dir():
        new_name_f = temp_folder.parent / new_name
        os.replace(temp_folder, new_name_f)
    else:
        new_name_f = temp_folder.parent / (new_name + suffix)
        os.replace(temp_folder, new_name_f)
    return new_name_f

def move_my_files(temp_folder):
    new_name = normalize(temp_folder.name)
    if new_name != temp_folder.name:
        temp_folder = Path(temp_folder.parent / new_name)
    
    for this_file in list_file:
        name_tf = this_file.pop('name')
        parent_tf = this_file.pop('parent')
        suffix_tf = this_file.pop('suffix')
        group_tf = this_file.pop('group')
        if group_tf == 'other':
            continue

        old_name_f = parent_tf / name_tf
        new_name_f = temp_folder / group_tf / name_tf
        if not os.path.exists(temp_folder / group_tf):
            os.mkdir(temp_folder / group_tf, 0o777)
        os.replace(old_name_f, new_name_f)
        if group_tf == 'archives':
            shutil.unpack_archive(new_name_f, temp_folder / group_tf / name_tf.rstrip(suffix_tf))
            os.remove(new_name_f)

def remove_empty_dirs(path):
    new_name = normalize(path.name)
    if new_name != path.name:
        path = Path(path.parent / new_name)
    
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if os.path.isdir(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)        
        

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

list_image = ['JPEG', 'PNG', 'JPG', 'SVG']
list_video = ['AVI', 'MP4', 'MOV', 'MKV']
list_doc = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
list_music = ['MP3', 'OGG', 'WAV', 'AMR']
list_zip = ['ZIP', 'GZ', 'TAR', '7z']

list_file = []
list_extensions = set()
list_unknown_extensions = set()

def main(): 
    temp_folder = Path(sys.argv[1])
    analysis_my_files(temp_folder)
    move_my_files(temp_folder)
    remove_empty_dirs(temp_folder)

if __name__ == "__main__":
    main()