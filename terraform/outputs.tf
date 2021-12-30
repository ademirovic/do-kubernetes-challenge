output "cluster_id" {
  description = "DO Kubernetes cluster ID"
  value       = digitalocean_kubernetes_cluster.cluster.id
}
