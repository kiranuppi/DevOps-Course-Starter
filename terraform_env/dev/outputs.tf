output "test_cosmosdb_connection_string" {
    value = "mongodb://${data.azurerm_cosmosdb_account.main.name}:${data.azurerm_cosmosdb_account.main.primary_key}@${data.azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@${data.azurerm_cosmosdb_account.main.name}@"
    sensitive = true
}