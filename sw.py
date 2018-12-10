#!/usr/bin/python3

'''Manages SSH servers'''
import sys
from os import path
import subprocess
import json


VERSION = '0.1.0'
DATA_DIR = path.join(path.expanduser('~'), '.sw')
KEYRING_PATH = path.join(DATA_DIR, 'keyring.json')


def print_version(*_args):
    print(VERSION)


def save_keyring(keyring):
    with open(KEYRING_PATH, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(keyring))


def list_keys(keyring):
    print('LABEL\tADDRESS')
    for key, addr in keyring.items():
        print('{0}\t{1}'.format(key, addr))
    return keyring


def add_key(keyring, label, addr):
    if label in keyring:
        print('The label {0} is already registered!'.format(label))
        return keyring
    keyring[label] = addr
    return keyring


def rename_key(keyring, label, new_label):
    if not add_key(new_label, keyring[label]):
        return keyring
    if not remove_key(label):
        return keyring
    return keyring


def remove_key(keyring, label):
    if label not in keyring:
        print('The label {0} does not exist!'.format(label))
        return keyring
    keyring.pop(label)
    return keyring


def ssh_connect(keyring, label):
    print('Connecting to {0}...'.format(keyring[label]))
    subprocess.run('ssh {0}'.format(keyring[label]), shell=True)
    print('ssh session finished')
    return keyring


def export_keyring(keyring):
    print(json.dumps(keyring))
    return keyring


def import_keyring(keyring, filepath):
    print('Merging current keyring and external keyring...')
    with open(filepath, 'r', encoding='utf-8') as f:
        new_keys = json.loads(f.read())
    return {**keyring, **new_keys}


commands = {
    'version': print_version,
    'list': list_keys,
    'add': add_key,
    'rename': rename_key,
    'remove': remove_key,
    'connect': ssh_connect,
    'export': export_keyring,
    'import': import_keyring,
}


def print_usage():
    print('USAGE: sw COMMAND')
    print()
    print('Possible commands:')
    print()
    print('sw list')
    print('sw add       LABEL   ADDR')
    print('sw rename    LABEL   NEWLABEL')
    print('sw remove    LABEL')
    print('sw connect   LABEL')
    print('sw export')
    print('sw import    FILE')


def main():
    if len(sys.argv) == 1:
        print_usage()
        exit()

    command = sys.argv[1]
    if command not in commands.keys():
        print_usage()
        exit()

    subprocess.run('mkdir -p ' + DATA_DIR, shell=True)
    try:
        with open(KEYRING_PATH, 'r', encoding='utf-8') as f:
            keyring = json.loads(f.read())
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        keyring = {}

    args = sys.argv[2:]
    keyring = commands[command](keyring, *args)

    save_keyring(keyring)


if __name__ == '__main__':
    main()
