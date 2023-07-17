# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"  # tested on v20230607.0.0
  config.vm.box_check_update = "false"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 1324  # default: 1024
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yaml"
    # ansible.verbose = "vvv"
  end

end
