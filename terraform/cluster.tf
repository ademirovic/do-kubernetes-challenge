data "digitalocean_kubernetes_versions" "cluster" {
  version_prefix = "1.21."
}


resource "digitalocean_kubernetes_cluster" "cluster" {
  name     = "${var.project_name}-cluster"
  region   = var.region
  version  = data.digitalocean_kubernetes_versions.cluster.latest_version
  vpc_uuid = digitalocean_vpc.vpc.id
  tags     = var.tags


  node_pool {
    name       = "${var.project_name}-worker-pool"
    size       = var.node_size
    node_count = var.node_count
    tags       = var.tags
  }
}
