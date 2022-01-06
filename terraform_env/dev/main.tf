terraform {
  required_providers {

    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
  backend "azurerm" {
    resource_group_name  = "OpenCohort1_KiranUppinkudru_ProjectExercise"
    storage_account_name = "ku13storage"
    container_name       = "ku13storage"
    key                  = "test.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmosdb-account"
  resource_group_name = var.resource_group_name
  location            = var.location
  offer_type          = "Standard"
  kind                = "MongoDB"
  capabilities {
    name = "EnableServerless"
  }
  capabilities {
    name = "EnableMongo"
  }
  mongo_server_version = "3.6"

  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  lifecycle { prevent_destroy = false }
}

data "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmosdb-account"
  resource_group_name = var.resource_group_name
  depends_on = [
    azurerm_cosmosdb_account.main,
  ]
}