# 1. Konfiguracja Providera (Mówimy Terraformowi, że gadamy z Azure)
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 2. Resource Group (Grupa Zasobów)
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_prefix}-dev"
  location = var.location
}

# 3. Storage Account (Konto Magazynu / Data Lake)
resource "azurerm_storage_account" "datalake" {
  name                     = "${var.project_prefix}datalakedev001" # Nazwa musi być unikalna w całym Azure i z małych liter!
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS" # Najtańsza replikacja, bo to środowisko DEV

  # TO JEST KLUCZOWE DLA DATA ENGINEERÓW:
  is_hns_enabled           = true 
}

# 4. Kontenery na dane (Systemy plików w Data Lake)
resource "azurerm_storage_data_lake_gen2_filesystem" "raw" {
  name               = "raw"
  storage_account_id = azurerm_storage_account.datalake.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "gold" {
  name               = "gold"
  storage_account_id = azurerm_storage_account.datalake.id
}

# 5. Output (Co Terraform ma nam wypluć na koniec)
output "datalake_primary_key" {
  value     = azurerm_storage_account.datalake.primary_access_key
  sensitive = true # Ukrywamy w konsoli, bo to hasło
}