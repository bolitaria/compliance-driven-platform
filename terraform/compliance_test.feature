# Terraform-compliance checks

Feature: Compliance-as-Code for infrastructure

  Scenario: Storage accounts must enforce HTTPS only
    Given I have azurerm_storage_account defined
    Then it must have enable_https_traffic_only set to true

  Scenario: Storage accounts must use TLS 1.2 or higher
    Given I have azurerm_storage_account defined
    Then it must have min_tls_version set to "TLS1_2"

  Scenario: AKS cluster must use system-assigned managed identity
    Given I have azurerm_kubernetes_cluster defined
    Then it must have identity
    And its identity must have type set to "SystemAssigned"