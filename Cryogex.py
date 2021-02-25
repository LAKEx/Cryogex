import subprocess
import sys
import os
import json
import shlex
from pathlib import Path
import signal
import sys

config_path = str(Path(os.getcwd() + '/' + str(Path('Cryogex.json'))))


config_data = {
    'global': {}
}
try:
    config_file = open(config_path)
    config_data = json.load(config_file)
    config_file.close()
except:
    config_file = open(config_path, 'w')
    config_file.write(json.dumps(config_data))
    config_file.close()

run = True

while run:
    print('>:', end=' ')
    command = None
    try:
        command = input().strip()
    except KeyboardInterrupt:
        print()
        continue

    split_command = shlex.split(command)
    modified_command_list = []
    tmp = []
    for part in split_command:
        if part == '&&' and len(tmp):
            modified_command_list.append(tmp)
            tmp = []
            continue
        if os.path.isfile(part):
            new_file_path = os.getcwd() + '/' + str(Path(part))
            new_file_path = str(Path(new_file_path))
            tmp.append(new_file_path)
        else:
            tmp.append(part)
    if len(tmp):
        modified_command_list.append(tmp)
    for com in modified_command_list:
        if len(com) == 1 and com[0] == 'exit':
            exit()
        try:
            if len(com) == 2 and com[0] == 'cd':
                os.chdir(com[1])
            elif len(com) == 1 and com[0] == 'curdir':
                print(os.getcwd())
            elif len(com) >= 1 and com[0] == '-gs':
                alias = None
                command_to_save = None
                try:
                    print()
                    print('Enter One-Word Command Alias:', end=' ')
                    alias = input()
                    print('Enter Command:', end=' ')
                    command_to_save = input()
                    array_to_save = shlex.split(command_to_save)
                    tmp_to_save = []
                    for to_save_part in array_to_save:
                        if os.path.isfile(to_save_part):
                            if '-lf' in com:
                                tmp_to_save.append(str(Path(to_save_part)))
                            else:
                                tmp_to_save.append(
                                    str(Path(os.getcwd() + '/' + str(Path(to_save_part)))))
                        else:
                            tmp_to_save.append(to_save_part)
                    command_to_save = ' '.join(tmp_to_save)
                    print()
                except KeyboardInterrupt:
                    print()
                    print()
                    continue
                try:
                    config_data['global'][alias] = command_to_save
                    config_file = open(config_path, 'w')
                    config_file.write(json.dumps(config_data))
                    config_file.close()
                except:
                    print('Command failed to save!')
            elif len(com) > 0:
                try:
                    subprocess.run(shlex.split(
                        config_data['global'][com[0]]) + com[1:])
                except:
                    subprocess.run(com)
        except Exception as e:
            pass
