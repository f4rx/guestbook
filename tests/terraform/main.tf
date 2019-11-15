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

module "app-stand" {
  source = "https://github.com/f4rx/app-terraform.git?ref=master"

  region                = "${var.region}"
  public_key            = "${var.public_key}"
  hdd_size              = "${var.hdd_size}"
  volume_type           = "${var.volume_type}"
  az_zone               = "${var.az_zone}"
  app_count             = "1"

  domain_name = "${var.domain_name}"
  project_id = "${var.project_id}"
  user_name = "${var.user_name}"
  user_password = "${var.user_password}"

}

output "server_external_ip" {
  value = "${module.app-stand.server_external_ip}"
}
