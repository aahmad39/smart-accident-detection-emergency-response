output "sql_server_id" {
  value       = azurerm_mssql_server.sql_server.id
  description = "SQL Server ID"
}

output "sql_server_fqdn" {
  value       = azurerm_mssql_server.sql_server.fully_qualified_domain_name
  description = "SQL Server FQDN"
}

output "database_id" {
  value       = azurerm_mssql_database.database.id
  description = "SQL Database ID"
}

output "database_name" {
  value       = azurerm_mssql_database.database.name
  description = "SQL Database Name"
}

output "connection_string" {
  value       = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.sql_server.fully_qualified_domain_name},1433;Database=${azurerm_mssql_database.database.name};Uid=${azurerm_mssql_server.sql_server.administrator_login};Pwd=${random_password.sql_admin_password.result};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
  sensitive   = true
  description = "ODBC connection string for Flask app"
}
