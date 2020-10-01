#!/usr/bin/env python3
#
# Utility to generate the collection requirements for an existing
# Ansible Playbook written prior to Ansible 2.10 being released
#
# Written By: Nick Thompson (@nsthompson)
# Copyright (C) 2020 World Wide Technology
# All Rights Reserved
#

import sys
import os.path
from lib.runtime import LoadRuntime
from ruamel.yaml import YAML
from ansible.playbook import Playbook
from ansible.playbook.task import Task
from ansible.parsing.dataloader import DataLoader


def get_collections(playbook_data):
    # Instantiate runtime class
    runtime = LoadRuntime()

    # Build the Lists of Valid Attributes
    valid_task_attrs = list(Task()._valid_attrs.keys())

    # Define an empty dict for the loop
    collection_dict = {}

    # Define a counter for the loop
    play_id = 1

    # Get Collection Information
    for play in playbook_data:

        # Define our collection set
        collection_set = set()

        for task in play['tasks']:
            for key in list(task.keys()):
                if key not in valid_task_attrs:
                    new_fqcn = runtime.get_module_fqcn(key)
                    if new_fqcn != "":
                        # print(f'{module} -> {new_fqcn}')
                        new_collection = ".".join(new_fqcn.split(".", 2)[:2])
                        collection_set.add(new_collection)
        # Create our Collection Dict
        collections = {
            "collections": list(collection_set)
        }

        # Add the Data to collection_dict
        collection_dict[play_id] = collections

        play_id += 1

    return(collection_dict)


def main():
    try:
        playbook_arg = sys.argv[1]
    except IndexError:
        print("Playbook Path is Required")
        sys.exit(1)

    if os.path.isfile(playbook_arg):
        playbook_path = os.path.abspath(playbook_arg)
    else:
        print("Playbook is missing!")
        sys.exit(1)

    yaml = YAML()

    # Load and Parse our Playbook
    loader = DataLoader()
    playbook = Playbook.load(playbook_path, loader=loader)

    # Build the List of Playbook Dictionaries
    playbook_dict = playbook._loader.__dict__['_FILE_CACHE'][playbook_path]

    # Parse The Playbook
    collections = get_collections(playbook_dict)

    # Dump YAML of new collections
    for key in collections.keys():
        print(f'# Play {key}')
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(collections[key], sys.stdout)


if __name__ == "__main__":
    main()
