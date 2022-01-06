variable "prefix" {
  type        = string
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  type        = string
  description = "The Azure location where all resources in this  deployment should be created"
}

variable "resource_group_name" {
  type = string
  description = "The Azure resource name where all resources in this deployment should be created"

}