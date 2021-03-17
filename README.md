# Ansible Role: MySQL
[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/ansible-role-mysql/master/LICENSE)
[![Build status](https://gitlab.com/lean-delivery/ansible-role-mysql/badges/master/pipeline.svg)](https://gitlab.com/lean-delivery/ansible-role-mysql/-/commits/master)
[![Galaxy](https://img.shields.io/badge/galaxy-lean__delivery.mysql-blue.svg)](https://galaxy.ansible.com/lean_delivery/mysql)
![Ansible](https://img.shields.io/ansible/role/d/35413.svg)
![Ansible](https://img.shields.io/badge/dynamic/json.svg?label=min_ansible_version&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F35413%2F&query=$.min_ansible_version)

## Summary

This role installs and configures MySQL or MariaDB server on RHEL/CentOS servers.

## Role tasks

  - Installs MySQL/MariaDB
  - Reset root password for mysql
  - Create db and users

## Requirements

  - Supported versions:
      - Oracle Mysql
          - 5.5
          - 5.6
          - 5.7
          - 8.0
      - Mariadb
          - 10.3
          - 10.4
          - 10.5
  - Supported OS:
      - RHEL
          - 7
          - 8
      - CentOS
          - 7
          - 8
      - Ubuntu
          - 18.04
      - Debian
          - 9
          - 10

## Role Variables

Available variables are listed below, along with default values:

Mysql/MariaDB repository settings:

    mysql_repo: *default value depends on OS*   
    mysql_gpgkey: *default value depends on OS*   
    mysql_apt_keyserver: *default value depends on OS*  
    mysql_repofile: /etc/yum.repos.d/mysql.repo|/etc/yum.repos.d/mariadb.repo
    mysql_apt_key_id: *default value depends on OS*   
    mysql_repo_disable_list: *default - undefined*. For CentOS 8 it's now list of `AppStream` and `Stream-AppStream`.

    mysql_packages:
      - mysql-community-server   # (mysql-community-server/MariaDB-server)
      - mysql-community-client   # (mysql-community-client/MariaDB-client)
      
If you want to select a specific minor version of package, you can enter appropriate package name, for instance:

    mysql_packages:
      - mysql-community-server-8.0.16-2.el7.x86_64
      - mysql-community-client-8.0.16-2.el7.x86_64

Alternatively, you can define the packages as a list of external urls by setting the variable `mysql_artifacts`, e.g.:

    mysql_artifacts:
      - https://downloads.mysql.com/archives/get/p/23/file/mysql-community-client_5.7.31-1ubuntu18.04_amd64.deb
      - https://downloads.mysql.com/archives/get/p/23/file/mysql-community-server_5.7.31-1ubuntu18.04_amd64.deb
      
### NOTE: *This option was tested only for deb-based packages at the moment.*
                                 # (MariaDB-common)
    mysql_daemon: mysqld         # (mysqld/mariadb)
    mysql_version: 5.7           # (for mysql = 5.5/5.6/5.7; for mariadb = last (10.5) )

(OS-specific, RedHat/CentOS defaults listed here) Packages to be installed. In some situations, you may need to add additional packages, like `mysql-devel`.

    mysql_user_home: /root
    mysql_user_name: root
    mysql_user_password: root

The home directory inside which Python MySQL settings will be stored, which Ansible will use when connecting to MySQL. This should be the home directory of the user which runs this Ansible role. The `mysql_user_name` and `mysql_user_password` can be set if you are running this role under a non-root user account and want to set a non-root user.

    mysql_root_home: /root
    mysql_root_username: root
    mysql_root_password: root

The MySQL root user account details.

    mysql_config_file: *default value depends on OS*
    mysql_config_include_dir: *default value depends on OS*
    
The main my.cnf configuration file and include directory.

    overwrite_global_mycnf: true

Whether the global my.cnf should be overwritten each time this role is run. Setting this to `no` tells Ansible to only create the `my.cnf` file if it doesn't exist. This should be left at its default value (`yes`) if you'd like to use this role's variables to configure MySQL.

    mysql_config_include_files: []

A list of files that should override the default global my.cnf. Each item in the array requires a "src" parameter which is a path to a file. An optional "force" parameter can force the file to be updated each time ansible runs.

    mysql_databases: []

The MySQL databases to create. A database has the values `name`, `encoding` (defaults to `utf8`), `collation` (defaults to `utf8_general_ci`) and `replicate` (defaults to `1`, only used if replication is configured). The formats of these are the same as in the `mysql_db` module.

    mysql_users: []

The MySQL users and their privileges. A user has the values:

  - `name`
  - `host` (defaults to `localhost`)
  - `password` (can be plaintext or encrypted—if encrypted, set `encrypted: yes`)
  - `encrypted` (defaults to `no`)
  - `priv` (defaults to `*.*:USAGE`)
  - `append_privs` (defaults to `no`)
  - `state`  (defaults to `present`)

The formats of these are the same as in the `mysql_user` module.

    mysql_port: "3306"
    mysql_bind_address: '0.0.0.0'
    mysql_datadir: /var/lib/mysql
    mysql_socket: *default value depends on OS*
    mysql_pid_file: *default value depends on OS*

Default MySQL connection configuration.

    mysql_log_file_group: mysql *adm on Debian*
    mysql_log: ""
    mysql_log_error: *default value depends on OS*
    mysql_syslog_tag: *default value depends on OS*

MySQL logging configuration. Setting `mysql_log` (the general query log) or `mysql_log_error` to `syslog` will make MySQL log to syslog using the `mysql_syslog_tag`.

    mysql_slow_query_log_enabled: false
    mysql_slow_query_log_file: *default value depends on OS*
    mysql_slow_query_time: 2

Slow query log settings. Note that the log file will be created by this role, but if you're running on a server with SELinux or AppArmor, you may need to add this path to the allowed paths for MySQL, or disable the mysql profile. For example, on Debian/Ubuntu, you can run `sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/usr.sbin.mysqld && sudo service apparmor restart`.

    mysql_key_buffer_size: "256M"
    mysql_max_allowed_packet: "64M"
    mysql_table_open_cache: "256"
    [...]

The rest of the settings in `defaults/main.yml` control MySQL's memory usage and some other common settings. The default values are tuned for a server where MySQL can consume ~512 MB RAM, so you should consider adjusting them to suit your particular server better.

    mysql_server_id: "1"
    mysql_max_binlog_size: "100M"
    mysql_binlog_format: "ROW"
    mysql_expire_logs_days: "10"
    mysql_replication_role: ''
    mysql_replication_master: ''
    mysql_replication_user: []

Replication settings. Set `mysql_server_id` and `mysql_replication_role` by server (e.g. the master would be ID `1`, with the `mysql_replication_role` of `master`, and the slave would be ID `2`, with the `mysql_replication_role` of `slave`). The `mysql_replication_user` uses the same keys as `mysql_users`, and is created on master servers, and used to replicate on all the slaves.

`mysql_replication_master` needs to resolve to an IP or a hostname which is accessable to the Slaves (this could be a `/etc/hosts` injection or some other means), otherwise the slaves cannot communicate to the master.

## additional_parameters
Also you can set other parametrs, which are not listed here and it will be written to the configuration file `my.cnf`. 

Example:
```yaml
     additional_parameters:
        - name: mysql_expire_logs_days
          value: 11
```
#

### MariaDB usage

This role works with either MySQL or a compatible version of MariaDB. On RHEL/CentOS 7+, the mariadb database engine was substituted as the default MySQL replacement package. No modifications are necessary though all of the variables still reference 'mysql' instead of mariadb.

## Dependencies

Due to new breaking changes in MySQL 8.0 we included modified module `mysql_user`. It's shipping with that role and resides in `library` directory. Current Ansible module `mysql_user` is not compatible with latest changes but fixes are already in place and new Ansible release 2.8 should not require customized module to run.

## Example Playbooks

### Installing MySQL 5.7 version:
```yaml
- hosts: db-servers
  roles:
    - role: lean_delivery.mysql
  vars:
    mysql_root_password: Super_P@s$0rd
    mysql_databases:
      - name: example2_db
        encoding: latin1
        collation: latin1_general_ci
    mysql_users:
      - name: example2_user
        host: "%"
        password: Sime32_U$er_p@ssw0rd
        priv: "example2_db.*:ALL"
    mysql_port: 3306
    mysql_bind_address: '0.0.0.0'
    mysql_daemon: mysqld
    mysql_version: 5.7
``` 

### Installing MySQL 8.0 version:
```yaml
- hosts: db-servers
  roles:
    - role: lean_delivery.mysql
  vars:
    mysql_root_password: 88TEM-veDRE<888serd
    mysql_databases:
      - name: example2_db
        encoding: latin1
        collation: latin1_general_ci
    mysql_users:
      - name: example2_user
        host: "%"
        password: Sime32-SRRR-password
        priv: "example2_db.*:ALL"
    mysql_port: 3306
    mysql_bind_address: '0.0.0.0'
    mysql_daemon: mysqld
    mysql_version: 8.0
    mysql_packages:
      - mysql-server
``` 

### Installing MariaDB:
```yaml
- hosts: db-servers
  roles:
    - role: lean_delivery.mysql
  vars:
    mysql_root_password: 88TEM-veDRE<888serd
    mysql_databases:
      - name: example2_db
        encoding: latin1
        collation: latin1_general_ci
    mysql_users:
      - name: example2_user
        host: "%"
        password: Sime32-SRRR-password
        priv: "example2_db.*:ALL"
    mysql_port: 3306
    mysql_bind_address: '0.0.0.0'
    mysql_daemon: mariadb
``` 


__Note__: CentOS always do password reset via `rescue` section: It should be noted that the play continues if a rescue section completes successfully as it ‘erases’ the error status (but not the reporting), this means it will appear in the **playbook statistics** ONLY.

**ATTENTION!** Note that override parameters in playbook have to be set as `role parameters` (see example above). Parameters set as usual hostvars or inventory parameters will not supercede default role parameters set by role scenario depending on OS version etc. 

## License
Apache


## Author Information
authors:

  - Lean Delivery Team team@lean-delivery.com
