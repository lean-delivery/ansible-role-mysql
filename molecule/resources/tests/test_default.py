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
    name = host.ansible("setup")["ansible_facts"]["mysql_service_name"]
    with host.sudo():
        service = host.service(name)
        assert service.is_running
        assert service.is_enabled

def test_mysql_is_listening(host):
    assert host.socket('tcp://127.0.0.1:3306').is_listening
