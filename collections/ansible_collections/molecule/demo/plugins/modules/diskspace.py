#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = ''' 
module: diskspace
short_description: Diskspace utilistation status
version_added: "0.1"
description:
    - This shows how much a directory utilising space and reside on which disk
options:
    path:
        description:
            - Path of directory or file
        type: str
        required: true
    storage:
        description:
            - A boolean value to display storage name where directory/file resides
        required: false
        type: bool
        default: no

author:
- Mitesh The Mouse (mitsharm@redhat.com)
'''
EXAMPLES = '''
# Shows /tmp disk utilisation 
- name: Test with a message
  diskspace:
    path: /tmp
# Shows /tmp disk utilisation and storage location
- name: Test with a message
  diskspace:
    path: /tmp
    storage: True
'''

import os
import stat
import subprocess
from ansible.module_utils.basic import AnsibleModule

def diskspace():
    module_args = dict( 
      path = dict(type='str', required=True),
      storage =  dict(type='bool', required=False, default=False)
      )

    module = AnsibleModule(
      argument_spec=module_args,
      supports_check_mode=True
      )

    result = dict(
       failed = False, 
       changed=False,
       stdout = '',
       stdout_line='',
       stderr_line='',
       device=''
       )

    if os.path.exists(module.params['path']):
      if os.path.isdir(module.params['path']):
        
        #######################################################  
        # Calculating disk usages
        dump_du_output = subprocess.Popen(["du", "-chd  1", module.params['path']], stdout=subprocess.PIPE ).communicate()[0]
        for lines in dump_du_output.split("\n"):
          if len(lines) > 0:
            if lines.split()[1] == "total" :
              result['stdout'] = lines
        
        result['stdout_line'] = dump_du_output
        result['changed'] = True
        #######################################################
        # finding directory storage path
        storage_path = subprocess.Popen(["df", "-P", module.params['path']], stdout=subprocess.PIPE ).communicate()[0]
        if module.params['storage']:
          for device_list in storage_path.split("\n"):
            if len(device_list.split()) > 0:
              if device_list.split()[0] != "Filesystem":
                result['device'] = module.params['path'] + " " + " is reside on " + device_list.split()[0]
       
      else:
        result['stderr_line'] = module.params['path'] + " " + "is not directory"
        result['failed'] = True
    else:
      result['stderr_line'] = module.params['path'] + " " + "does not exist"
      result['failed'] = True

    module.exit_json(**result)


def main():
  diskspace()

if __name__ == '__main__':
    main()
