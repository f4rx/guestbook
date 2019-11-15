variable "domain_name" {}
variable "project_id" {}
variable "user_name" {}
variable "user_password" {}
variable "region" {}
variable "az_zone" {}
variable "volume_type" {}
variable "public_key" {}
variable "hdd_size" {
  default = "5"
}


provider "openstack" {
  domain_name = "${var.domain_name}"
  tenant_id   = "${var.project_id}"
  user_name   = "${var.user_name}"
  password    = "${var.user_password}"
  auth_url    = "https://api.selvpc.ru/identity/v3"
  region      = "${var.region}"
}

###################################
# Flavor
###################################
data "openstack_compute_flavor_v2" "flavor_1" {
  name = "SL1.1-1024"
}

###################################
# Get image ID
###################################
data "openstack_images_image_v2" "ubuntu" {
  most_recent = true
  name        = "Ubuntu 16.04 LTS 64-bit"
}

###################################
# Create SSH-key
###################################
resource "openstack_compute_keypair_v2" "terraform_key" {
  name       = "terraform_key-${var.project_id}"
  region     = "${var.region}"
  public_key = "${var.public_key}"
}

###################################
# Create Network and Subnet
###################################
data "openstack_networking_network_v2" "external_net" {
  name = "external-network"
}

resource "openstack_networking_router_v2" "router_1" {
  name                = "router_1"
  external_network_id = "${data.openstack_networking_network_v2.external_net.id}"
}

resource "openstack_networking_router_interface_v2" "router_interface_1" {
  router_id = "${openstack_networking_router_v2.router_1.id}"
  subnet_id = "${openstack_networking_subnet_v2.subnet_1.id}"
}

resource "openstack_networking_network_v2" "network_1" {
  name = "network_1"
}

resource "openstack_networking_subnet_v2" "subnet_1" {
  network_id      = "${openstack_networking_network_v2.network_1.id}"
  name            = "192.168.0.0/24"
  cidr            = "192.168.0.0/24"
  dns_nameservers = ["188.93.16.19", "188.93.17.19"]
}

###################################
# Create port
###################################
resource "openstack_networking_port_v2" "port_1" {
  name       = "node-eth0"
  network_id = "${openstack_networking_network_v2.network_1.id}"

  fixed_ip {
    subnet_id = "${openstack_networking_subnet_v2.subnet_1.id}"
  }
}

###################################
# Create Volume/Disk
###################################
resource "openstack_blockstorage_volume_v3" "volume_1" {
  name                 = "volume-for-node"
  size                 = "${var.hdd_size}"
  image_id             = "${data.openstack_images_image_v2.ubuntu.id}"
  volume_type          = "${var.volume_type}"
  availability_zone    = "${var.az_zone}"
  enable_online_resize = true

  lifecycle {
    ignore_changes = ["image_id"]
  }
}
###################################
# Create Server
###################################
resource "openstack_compute_instance_v2" "instance_1" {
  name              = "node"
  flavor_id         = "${data.openstack_compute_flavor_v2.flavor_1.id}"
  key_pair          = "${openstack_compute_keypair_v2.terraform_key.id}"
  availability_zone = "${var.az_zone}"

  network {
    port = "${openstack_networking_port_v2.port_1.id}"
  }

  block_device {
    uuid             = "${openstack_blockstorage_volume_v3.volume_1.id}"
    source_type      = "volume"
    destination_type = "volume"
    boot_index       = 0
  }

  vendor_options {
    ignore_resize_confirmation = true
  }

  provisioner "file" {
    content = <<-EOT
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

apt-get update

apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

apt-get install -y docker-ce docker-ce-cli containerd.io

apt install -y python3-pip python3-setuptools python3-wheel

pip3 install docker-compose
EOT
    destination = "/tmp/setup_docker.sh"
    connection {
      type  = "ssh"
      host  = "${openstack_networking_floatingip_v2.floatingip_1.address}"
      user  = "root"
      # private_key = "${file("~/.ssh/id_rsa")}"
      #agent = true
    }
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup_docker.sh",
      "/tmp/setup_docker.sh",
    ]

    connection {
      type = "ssh"
      host  = "${openstack_networking_floatingip_v2.floatingip_1.address}"
      user  = "root"
      # private_key = "${file("~/.ssh/id_rsa")}"
    }
  }
}

###################################
# Create floating IP
###################################
resource "openstack_networking_floatingip_v2" "floatingip_1" {
  pool = "external-network"
}

###################################
# Link floating IP to internal IP
###################################
resource "openstack_networking_floatingip_associate_v2" "association_1" {
  port_id     = "${openstack_networking_port_v2.port_1.id}"
  floating_ip = "${openstack_networking_floatingip_v2.floatingip_1.address}"
}

output "server_external_ip" {
  value = "${openstack_networking_floatingip_v2.floatingip_1.address}"
}
