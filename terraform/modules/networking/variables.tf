variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
}

variable "location" {
  type        = string
  description = "Azure region (e.g. uksouth)"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, qa, uat, prod)"
}

variable "vnet_name" {
  type        = string
  description = "Name of the Virtual Network"
}

variable "address_space" {
  type        = list(string)
  default     = ["10.0.0.0/16"]
  description = "CIDR address space for the VNet"
}

variable "subnet_prefixes" {
  type        = map(string)
  default = {
    app = "10.0.1.0/24"
    db  = "10.0.2.0/24"
    pe  = "10.0.3.0/24"
  }
  description = "Subnet CIDR allocations"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}
