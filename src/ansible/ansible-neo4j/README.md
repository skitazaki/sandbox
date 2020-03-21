| [![Build Status](https://travis-ci.org/skitazaki/ansible-neo4j.svg?branch=develop)](https://travis-ci.org/skitazaki/ansible-neo4j) | [![CircleCI](https://circleci.com/gh/skitazaki/ansible-neo4j/tree/develop.svg?style=svg)](https://circleci.com/gh/skitazaki/ansible-neo4j/tree/develop) |
|-----|-----|

# Ansible playbook for Neo4j

*ansible-neo4j* is a Ansible playbook for Neo4j to install and configure [Neo4j Graph Database](https://neo4j.com/) server.

## Getting started

### Requirements

You have to manually spin up dedicated instance or you can use Vagrant with VirtualBox for local testing.

For dedicated environment, you should prepare two instances, one is Ansible control machine and the other is a remote node to run Neo4j server.
The remote node have to be configured to accept SSH connection from control machine.

- Ansible 2.3+ on control machine

If you just try on local machine, you have to install following softwares on your own.
Vagrant spins up Ansible control machine and uses Ansible Local provisioner to run playbook.

- VirtualBox
- Vagrant

### Usage for dedicated environment

```bash
$ ansible-galaxy install -r requirements.yml -p roles
$ ansible-playbook -i environments/development site.yml
```

### Usage for local machine

1. Clone this repository.
2. `vagrant up` to up and provision instances.
3. Neo4j server will be available at `http://192.168.20.20:7474` with default username/password pair, *neo4j*/*neo4j*.

To change IP address of Neo4j server, set *VAGRANT_NEO4J_IP* environmental variable.

## Developing

### Built with

- Ansible 2.3+
- Ansible Galaxy modules written in `requirements.yml`
- Ansible Lint
- VirtualBox
- Vagrant, Ansible Local provisioner
- Serverspec

### Setting up Dev

Clone the repository and spin up instances on VirtualBox.

```bash
$ git clone https://github.com/skitazaki/ansible-neo4j.git
$ cd ansible-neo4j/
$ vagrant up
```

Once provisioned, you can login to *controller* instance to run `ansible-playbook`.

```bash
$ vagrant ssh controller

> cd /opt/playbook
> ansible-playbook site.yml --list-hosts
```

### Test

Run Serverspec test suite on *controller* instance.

```bash
$ vagrant ssh controller

> cd /opt/playbook
> rake spec
```

Lint playbooks using `ansible-lint`.

```bash
$ vagrant ssh controller

> cd /opt/playbook
> ansible-lint vagrant.yml --exclude=roles
```

### CI services

This repository is connected with Travis CI and CicleCI.
On Travis CI, it runs playbooks and checks the provisioned server status.
On CircleCI, it lints playbooks not only syntax but also some rules.

## Configuration

You probably want to manage multiple environments such as *dev*, *stg*, and *prd*.
You can manage separated inventories and configurations in *environments/* and *vars/* directories respectively.
If you want to run Serverspec test suites on each environment, *spec/* directory holds skelton files.

Each inventory file have to define *env* variable so that playbook can load respective configuration files using *var_files*.
