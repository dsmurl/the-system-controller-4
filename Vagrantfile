# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    # Prefer VirtualBox provider.
    config.vm.provider "virtualbox"

    # Box configuration.
    config.vm.box = "debian-jessie"
    config.vm.box_url = "https://github.com/holms/vagrant-jessie-box/releases/download/Jessie-v0.1/Debian-jessie-amd64-netboot.box"

    # SSH configration.
    config.ssh.forward_x11 = true
    config.ssh.forward_agent = true

    # Network configration.
    config.vm.network "private_network", type: "dhcp"

    # Use the cachier plugin if available.
    if Vagrant.has_plugin?("vagrant-cachier")
        config.cache.scope = :box
    end

    # Use the landrush plugin if available.
    if Vagrant.has_plugin?("landrush")
        config.landrush.enabled = true
    end

    # Customize the virtualbox provider.
    config.vm.provider "virtualbox" do |v|
        v.memory = "1024"
    end

    # Create the box and provision it.
    config.vm.define "thesystemcontroller" do |thesystemcontroller|
        thesystemcontroller.vm.hostname = "thesystemcontroller.vagrant.dev"

        # Configure the port forwarding.
        thesystemcontroller.vm.network "forwarded_port", host: 8080, guest: 8080, auto_correct: true

        # Provision the box using an Ansible playbook.
        thesystemcontroller.vm.provision "ansible" do |ansible|
            ansible.playbook = "ansible/provision.yml"
            ansible.sudo = true
            ansible.verbose= ""
        end
    end
end
