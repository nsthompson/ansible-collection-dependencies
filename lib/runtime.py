#
# Class for parsing ansible_builtin_runtime.yml file
#
# Written By: Nick Thompson (@nsthompson)
# Copyright (C) 2020 World Wide Technology
# All Rights Reserved
#

import os
import yaml


class LoadRuntime:

    def __init__(self, log=None):

        self.log = log

        basepath = os.path.dirname(os.path.abspath(__file__))

        with open(f'{basepath}/ansible_builtin_runtime.yml') as runtime_file:
            self.runtime_info = yaml.load(runtime_file, Loader=yaml.SafeLoader)

    def get_module_fqcn(self, module_name):
        try:
            module_fqcn = (
                self.runtime_info['plugin_routing']
                ['modules']
                [f'{module_name}']
                ['redirect']
            )
        except KeyError:
            module_fqcn = ""

        return(module_fqcn)
