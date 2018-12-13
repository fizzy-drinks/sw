#!/usr/bin/python3

'''Manages SSH servers'''
import sys
from os import path
import subprocess
import json


VERSION = '0.2.0'
DATA_DIR = path.join(path.expanduser('~'), '.sw')
KEYRING_PATH = path.join(DATA_DIR, 'keyring.json')


def read_keyring(fn):
    def read_keyring_fn(*args, **kwargs):
        subprocess.run('mkdir -p ' + DATA_DIR, shell=True)
        try:
            with open(KEYRING_PATH, 'r', encoding='utf-8') as f:
                keyring = json.loads(f.read())
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            keyring = {}

        result = fn(*args, **kwargs, keyring=keyring)
        save_keyring(keyring)
        return result

    return read_keyring_fn


def required_argument_count(min_args):
    def required_argument_count_decorator(fn):
        def required_argument_count_decorator_fn(*args, **kwargs):
            if len(args) < min_args:
                print('This action requires {0} arguments!'.format(min_args))
                return
            return fn(*args, **kwargs)

        return required_argument_count_decorator_fn
    return required_argument_count_decorator


def print_version(*_args):
    print(VERSION)


def save_keyring(keyring):
    with open(KEYRING_PATH, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(keyring))


@read_keyring
def list_keys(keyring):
    print('LABEL\tADDRESS')
    for key, addr in keyring.items():
        print('{0}\t{1}'.format(key, addr))
    return keyring


@required_argument_count(2)
@read_keyring
def add_key(label, addr, keyring):
    if label in keyring:
        print('The label {0} is already registered!'.format(label))
        return keyring
    keyring[label] = addr
    return keyring


@required_argument_count(2)
@read_keyring
def rename_key(label, new_label, keyring):
    if not add_key(new_label, keyring[label]):
        return keyring
    if not remove_key(label):
        return keyring
    return keyring


@required_argument_count(1)
@read_keyring
def remove_key(label, keyring):
    if label not in keyring:
        print('The label {0} does not exist!'.format(label))
        return keyring
    keyring.pop(label)
    return keyring


@required_argument_count(1)
@read_keyring
def ssh_connect(label, keyring):
    if label not in keyring:
        print('{0} is not a valid label!'.format(label))
    else:
        print('Connecting to {0}...'.format(keyring[label]))
        subprocess.run('ssh {0}'.format(keyring[label]), shell=True)
        print('ssh session finished')
    return keyring


@required_argument_count(2)
@read_keyring
def ssh_run(label, command, keyring):
    if label not in keyring:
        print('{0} is not a valid label!'.format(label))
    else:
        print('Connecting to {0}...'.format(keyring[label]))
        subprocess.run('ssh -t {0} {1}'.format(keyring[label], command), shell=True)
        print('ssh session finished')
    return keyring


@read_keyring
def export_keyring(keyring):
    print(json.dumps(keyring))
    return keyring


@required_argument_count(1)
@read_keyring
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
    'run': ssh_run,
}


def print_usage():
    print('USAGE: sw COMMAND')
    print()
    print('Possible commands:')
    print()
    print('sw version')
    print('sw list')
    print('sw add       LABEL   ADDR')
    print('sw rename    LABEL   NEWLABEL')
    print('sw remove    LABEL')
    print('sw connect   LABEL')
    print('sw run       LABEL   COMMAND')
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

    args = sys.argv[2:]
    keyring = commands[command](*args)


if __name__ == '__main__':
    main()
