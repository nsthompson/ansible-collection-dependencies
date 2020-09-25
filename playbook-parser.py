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
from ruamel.yaml import YAML
from lib.runtime import LoadRuntime


def get_collections(playbook_data, runtime):
    # Define our Module Tuple
    # These are values that will be
    # skipped over as we parse the playbook
    module_tuple = ("name", "with_items", "register", "debug")

    # Define our collection set
    collection_set = set()

    for play in playbook_data:
        for task in play['tasks']:
            for module in task:
                if module not in module_tuple:
                    new_fqcn = runtime.get_module_fqcn(module)
                    if new_fqcn != "":
                        # print(f'{module} -> {new_fqcn}')
                        new_collection = ".".join(new_fqcn.split(".", 2)[:2])
                        collection_set.add(new_collection)

    # Create our Collection Dict
    collections = {
        "collections": list(collection_set)
    }

    return(collections)


def main():
    try:
        playbook_path = sys.argv[1]
    except IndexError:
        print("Playbook Path Required")
        sys.exit(1)

    yaml = YAML()

    # Open Playbook for Parsing
    with open(f'{playbook_path}') as file:
        playbook_data = yaml.load(file)

    # Instantiate runtime class
    runtime = LoadRuntime()

    # Parse The Playbook
    collections = get_collections(playbook_data, runtime)

    # Dump YAML of new collections
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.dump(collections, sys.stdout)


if __name__ == "__main__":
    main()
