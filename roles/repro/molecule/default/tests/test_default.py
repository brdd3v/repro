"""Role testing files using testinfra."""

import pytest


def test_system_info(host):
    assert host.system_info.type == "linux"
    assert host.system_info.distribution == "ubuntu"
    assert host.system_info.release == "18.04"


@pytest.mark.parametrize("package_name", [
    "mysql-server", "python3-pip"
])
def test_apt_package_is_installed(host, package_name):
    assert host.package(package_name).is_installed


@pytest.mark.parametrize("package_name", [
    "pandas", "psutil", "PyMySQL"
])
def test_pip_package_is_installed(host, package_name):
    assert host.pip_package(pip_path="/usr/bin/pip3", 
                            name=package_name).is_installed


def test_mysql_is_active(host):
    assert host.service("mysql").is_running


def test_options_file_is_in_home_dir(host):
    assert host.file("/home/vagrant/.my.cnf").exists


def test_run_mysql_client_without_password(host):
    cmd = host.run("mysql")
    assert cmd.succeeded


def test_mysqldiff_is_installed(host):
    file_path = "/usr/local/bin/mysqldiff"
    assert host.file(file_path).exists
    assert host.file(file_path).is_executable
