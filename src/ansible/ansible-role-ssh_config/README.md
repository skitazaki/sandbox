# Ansible role ssh_config

[![Build Status](https://travis-ci.org/skitazaki/ansible-role-ssh_config.svg?branch=master)](https://travis-ci.org/skitazaki/ansible-role-ssh_config)

An Ansible Role that creates SSH client config file.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

Either of *ssh_config_targets* or *ssh_config_bastion_alias* is mandatory.

Target hosts are listed in the form of array of objects.
Each object must have *alias* property while other properties are optional.

```yaml
ssh_config_targets:
  - alias: "srv1"
    host: "192.168.0.11"
    port: 22
    user: username
    key: ~/.ssh/keys/secret.pem
```

If you use bastion host before target instances, you can use *ssh_config_bastion_\** variables.
`vars/aws.yml` shows AWS bastion pattern.
If you enable AWS pattern, set *ssh_config_aws* *yes* and define
*ssh_config_bastion_host*, *ssh_config_aws_bastion_key*, and *ssh_config_aws_target_key* variables.
An example is in `tests/vars/aws.yml`.

## Dependencies

None

## Example Playbook

```yaml
- hosts: localhost
  vars_files:
    - vars/main.yml
  roles:
    - role: skitazaki.ssh_config
```

## License

MIT
