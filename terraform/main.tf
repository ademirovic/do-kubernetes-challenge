variable "region" {
  type = string
}
variable "node_size" {
  type = string
}

variable "node_count" {
  type = number
}

variable "tags" {
  type = list(any)
}

variable "ip_range" {
  type = string
}

variable "project_name" {
  type = string
}
