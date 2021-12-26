terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
  backend "azurerm" {
    resource_group_name  = "OpenCohort1_KiranUppinkudru_ProjectExercise"
    storage_account_name = "ku13storage"
    container_name       = "ku13storage"
    key                  = "terraform.tfstate"
  }
}
provider "azurerm" {
  features {}
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmosdb-account"
  resource_group_name = var.RESOURCE_GROUP_NAME
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

  lifecycle { prevent_destroy = true }
}

data "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmosdb-account"
  resource_group_name = var.RESOURCE_GROUP_NAME
  depends_on = [
    azurerm_cosmosdb_account.main,
  ]
}


data "azurerm_resource_group" "main" {
  name = var.RESOURCE_GROUP_NAME
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-ku-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = var.linux_fx_version
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"          = var.DOCKER_REGISTRY_SERVER_URL
    "MONGO_CONNECTION_STRING"             = "mongodb://${data.azurerm_cosmosdb_account.main.name}:${data.azurerm_cosmosdb_account.main.primary_key}@${data.azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@${data.azurerm_cosmosdb_account.main.name}@"
    "DOCKER_REGISTRY_SERVER_PASSWORD"     = var.DOCKER_REGISTRY_SERVER_PASSWORD
    "DOCKER_REGISTRY_SERVER_USERNAME"     = var.DOCKER_REGISTRY_SERVER_USERNAME
    "GITHUB_CLIENT_ID"                    = var.GITHUB_CLIENT_ID
    "GITHUB_CLIENT_SECRET"                = var.GITHUB_CLIENT_SECRET
    "MONGODB_COLLECTION_NAME"             = var.MONGODB_COLLECTION_NAME
    "SECRET_KEY"                          = var.SECRET_KEY
    "OAUTHLIB_INSECURE_TRANSPORT"         = false
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = false

  }
  lifecycle { prevent_destroy = false }
}


