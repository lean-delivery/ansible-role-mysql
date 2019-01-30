import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_mysql_service(host):
    flag = False
    for service in ["mysql", "mariadb", "mysqld"]:
        with host.sudo():
            service = host.service(service)
            if service.is_running and service.is_enabled:
                flag = True
    assert flag


def test_mysql_is_listening(host):
    assert host.socket('tcp://127.0.0.1:3306').is_listening
