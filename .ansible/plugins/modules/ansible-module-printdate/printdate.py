#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '2.0',
                    'supported_by': 'community',
                    'status': ['preview']}

DOCUMENTATION = '''
---

'''

EXAMPLES = '''
- printdate:
    args_dt: "now"
    args_dt: "today"
    args_dt: "tomorrow"
    args_dt: "yesterday"
'''

RETURN = '''
INP
'''

# Python default imports
# import os
import time
# import re
# import subprocess
# import yaml

# Python Ansible imports
from ansible.module_utils.basic import AnsibleModule

def shell_exec(command):
    '''
    Execute raw shell command and return exit code and output
    '''
    cpt = subprocess.Popen(command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    output = []
    for line in iter(cpt.stdout.readline, ''):
        output.append(line)

    # Wait until process terminates (without using p.wait())
    while cpt.poll() is None:
        # Process hasn't exited yet, let's wait some
        time.sleep(0.5)

    # Get return code from process
    return_code = cpt.returncode

    # Return code and output
    return return_code, ''.join(output)


def normalize_input(input_data, input_data_name, module):
    '''
    Convert the date time accoording to input_data
    '''

    # Get chosen diff type
    # diff_type = module.params.get('diff')

    # Normalize yaml
    # if diff_type == 'yaml':
    #     ignore = module.params.get('diff_yaml_ignore')
    #     succ, input_data = normalize_yaml(input_data, ignore)
    #     if not succ:
    #         module.fail_json(msg="Convert to yaml failed on %s: %s" % (input_data_name, input_data))
    if input_data == 'now':
        return time.ctime()
    elif input_data == 'epoch':
        return time.ctime()
    elif input_data == 'tomorrow':
        return time.strftime('%d-%b-%Y %X',time.localtime(time.time()+(24*60*60)))
    elif input_data == 'yesterday': 
        return time.strftime('%d-%b-%Y %X',time.localtime(time.time()-(24*60*60*100)))
    else:
        module.fail_json(msg="Invalid input %s: %s" % (input_data_name, input_data))
    return input_data


def retrieve_input(direction, module):
    '''
    Retrieve and evaluate Ansible module input arguments.
    Input arguments:
      * args
    '''
    input_data_name = direction
    input_type_name = direction + '_type'

    input_data = module.params.get(input_data_name)
    input_type = module.params.get(input_type_name)

    # Input is a file
    if input_type == 'file':
        with open(input_data, 'rt') as fpt:
            input_data = fpt.read().decode("UTF-8")
    # Input is a command
    elif input_type == 'command':
        if module.check_mode:
            result = dict(
                changed=False,
                msg="This module does not support check mode when " +
                input_type_name + " is 'command'.",
                skipped=True
            )
            module.exit_json(**result)
        else:
            command = input_data
            ret, input_data = shell_exec(command)
            if ret != 0:
                module.fail_json(msg="%s command failed: %s" % (input_data_name, input_data))

    # Return evaluated input
    return input_data


def diff_module_validation(module):
    '''
    Validate for correct module call/usage in ansible.
    '''
    source = module.params.get('args_dt')


    # Validate ARGS
    if source not in ['now','epoch','tomorrow','yesterday']:
        # b_source = to_bytes(source, errors='surrogate_or_strict')
        # if not os.path.exists(b_source):
        #     module.fail_json(msg="source %s not found" % (source))
        # if not os.access(b_source, os.R_OK):
        #     module.fail_json(msg="source %s not readable" % (source))
        # if os.path.isdir(b_source):
        module.fail_json(msg="printdate does not support values: %s" % (source))

    # Validate target
    # if target_type == 'file':
    #     b_target = to_bytes(target, errors='surrogate_or_strict')
    #     if not os.path.exists(b_target):
    #         module.fail_json(msg="target %s not found" % (target))
    #     if not os.access(b_target, os.R_OK):
    #         module.fail_json(msg="target %s not readable" % (target))
    #     if os.path.isdir(b_target):
    #         module.fail_json(msg="diff does not support recursive diff of directory: %s" % (target))

    return module


def init_ansible_module():
    '''
    This is needed to Initialize Ansible Module.
    '''
    return AnsibleModule(
        argument_spec=dict(
            args_dt=dict(type='str', default="now",choices=['now','epoch', 'tomorrow', 'nextweek','yesterday']),
        ),
        supports_check_mode=True
    )


def main():
    '''
    The entry point to module
    '''
    # Initialize module
    module = init_ansible_module()

    # Validate module
    module = diff_module_validation(module)

    # Retrieve converted module input
    source = retrieve_input('args_dt', module)
    # target = retrieve_input('target', module)

    # Normalize input
    source_res = normalize_input(source, 'args_dt', module)
    # target = normalize_input(target, 'target', module)

    # Ansible printdate output
    printdate = {
        'inp':source,
        'results': source_res
    }
    # Did we have any changes?
    # changed = (source != "target")

    # Ansible module returned variables
    result = dict(printdate)

    # Exit ansible module call
    module.exit_json(result=result,changed=False)


if __name__ == '__main__':
    main()
# ANSIBLE_LIBRARY='/data01/ansible-learn/.ansible/plugins/modules' ansible -i hosts sp -m printdate -a 'args_dt=now'
