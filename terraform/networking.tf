resource "digitalocean_vpc" "vpc" {
  name     = "${var.project_name}-vpc"
  region   = var.region
  ip_range = "10.10.10.0/24"
}
