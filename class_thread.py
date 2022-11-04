from threading import Thread
import os
from pathlib import Path
import shutil
from locale import normalize


class File:
    def __init__(self, name, dir_address, sub_folder):
        self.name = name
        self.dir_address = dir_address
        self.sub_folder = sub_folder

    def __call__(self):
        original = os.path.join(self.dir_address, self.name)
        move_to = os.path.join(self.dir_address, self.sub_folder)
        shutil.move(original, move_to)
        splitted_name = self.name.split(".")
        new_name = normalize(self.name.replace(f'.{splitted_name[-1]}', ""))
        os.rename(os.path.join(f'{self.dir_address}\\{self.sub_folder}', self.name), os.path.join(
            f'{self.dir_address}\\{self.sub_folder}', f'{new_name}.{splitted_name[-1]}'))


class Archive:
    def __init__(self, name, dir_address):
        self.name = name
        self.dir_address = dir_address

    def __call__(self):
        splitted_name = self.name.split(".")
        new_name = normalize(
            self.name.replace(f'.{splitted_name[-1]}', ""))
        shutil.unpack_archive(os.path.join(self.dir_address, self.name),
                              os.path.join(f'{self.dir_address}\\archive', new_name))
        os.remove(os.path.join(self.dir_address, self.name))
        client_code(os.path.join(
            f'{self.dir_address}\\archive', f'{new_name}\\archive'))


def create_sub_folders(name):
    directories = ["images", "video", "documents", "archive", "audio"]
    for dir in directories:
        path = os.path.join(name, dir)
        os.mkdir(path)
    return directories


def client_code(name):
    directories = create_sub_folders(name)
    dir_address = Path(name)
    files = []
    for file in dir_address.iterdir():
        if file.name in directories:
            continue
        else:
            if file.is_dir():

                dir = os.listdir(file)
                if len(dir) == 0:
                    os.rmdir(os.path.join(dir_address, file.name))
                else:
                    client_code(os.path.join(dir_address, file.name))

            elif file.name.endswith(('.zip', 'gz', '.tar')):
                arch = Archive(file.name, dir_address)
                files.append(arch)

            elif file.name.endswith(('.jpeg', '.png', '.jpg', '.svg')):
                file_1 = File(file.name, dir_address, directories[0])
                files.append(file_1)

            elif file.name.endswith(('.avi', '.mp4', '.mov', '.mkv')):
                file_2 = File(file.name, dir_address, directories[1])
                files.append(file_2)

            elif file.name.endswith(('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')):
                file_3 = File(file.name, dir_address, directories[2])
                files.append(file_3)

            elif file.name.endswith(('.mp3', '.ogg', '.wav', '.amr')):
                file_4 = File(file.name, dir_address, directories[4])
                files.append(file_4)

    for file in files:
        Thread(target=file).start()


client_code("C:\\Users\\Андрей\\Desktop\\3")
