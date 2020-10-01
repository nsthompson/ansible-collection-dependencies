# ansible-collection-dependencies

This utility is used to generate the collection block for Playbooks using Ansible 2.10 and later by parsing Ansible 2.9 and earlier playbooks which will stop the warnings as Ansible 2.10 redirects the existing module to the new FQCN (fully qualified collection name).

**Usage:**

```shell
playbook-parser.py <path-to-playbook>
```

**Example 1:**

```shell
playbook-parser.py /development/playbooks/aci_demo_create.yml
```

**Example 1 Output:**

```yaml
# Play 1
collections:
  - cisco.aci
```

**Example 2:**

```shell
playbook-parser.py /development/playbooks/cisco_wlc/aireos_show_ap_summary_demo.yml
```

**Example 2 Output:**

```yaml
# Play 1
collections:
  - community.network
```

## Components

### playbook-parser.py

* Utility to parse ansible playbooks and generate required collections

### lib/ansible_builtin_runtime.yml

* This file is sourced from <https://github.com/ansible/ansible/blob/stable-2.10/lib/ansible/config/ansible_builtin_runtime.yml>
* To update this file do the following:
  
  ```shell
  wget https://raw.githubusercontent.com/ansible/ansible/stable-2.10/lib/ansible/config/ansible_builtin_runtime.yml
  ```

### lib/runtime.py

* Python class for parsing and searching the ansible_builtin_runtime.yml file

## Requirements

* Tested with Python 3.8.5

### Installing Python Requirements

```shell
pip install -r requirements.txt
```

## Contributors

* Nick Thompson (@nsthompson)
