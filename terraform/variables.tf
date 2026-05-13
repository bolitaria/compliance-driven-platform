
variable "resource_group_name" {
  description = "Azure resource group name"
  default     = "demo-platform-rg"
}

variable "location" {
  description = "Azure region"
  default     = "westeurope"
}

variable "cluster_name" {
  default = "demo-aks"
}

variable "node_count" {
  default = 2
}

variable "audit_storage_name" {
  description = "Globally unique name for the audit log storage account"
  default     = "auditlogssa2024"
}
