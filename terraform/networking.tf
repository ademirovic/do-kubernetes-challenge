resource "digitalocean_vpc" "vpc" {
  name     = "${var.project_name}-vpc"
  region   = var.region
  ip_range = var.ip_range
}
