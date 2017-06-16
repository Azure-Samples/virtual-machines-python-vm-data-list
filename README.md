---
services: virtual-machines
platforms: python
author: abhisekb
date: June, 2017
---

# Azure Management API IaaS VM Inventory Sample Scripts

This project contains several scripts that demonstrate how to use a simple
technique to extract, transform, and generate an inventory of virtual machines
(VMs) associated with a subscription. This will include VMs using both the Azure
Resource Manager (ARM) and Classic (ASM) deployment models.

Read the accompanying How-To Guide: 

-   [Using Azure Management APIs to Get Data About Your Deployed Resources](https://blogs.msdn.microsoft.com/azurecat/2017/06/14/using-azure-management-apis-to-get-data-about-your-deployed-resources/)

There are three main parts to the example code:

1.  An extraction process to pull the information on VMs directly from the Azure
    Management APIs using either PowerShell on Windows or the Azure CLI tool on
    Linux. This process produces several detailed JSON files.

2.  A transform process using Python scripts to combine and regularize the
    information extracted from the APIs, and output that data to a combined JSON
    file.

3.  An Inventory process to convert the transformed JSON file into easily
    readable CSV files.

## Prerequisites

-   [Python 3.0](https://www.python.org/downloads/) or higher

-   [Azure
    PowerShell](https://docs.microsoft.com/en-us/powershell/azure/install-azurerm-ps?view=azurermps-4.0.0)
    (if extracting using PowerShell for Windows)

-   [Azure CLI 1.0](https://docs.microsoft.com/en-us/azure/cli-install-nodejs)
    and [Azure CLI
    2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) if
    extracting using Linux

-   The [jq JSON processor](https://stedolan.github.io/jq/) is required if
    extracting using Linux

## Instructions 

Save the **samplecode** folder to a location on your local machine. This folder
contains a sample pyproj file and Visual Studio solution file for the project.
It also contains the following sub-folders:

-   extract - contains the PowerShell and Bash scripts used to extract
    information from the Azure Management APIs

-   transform - contains the transform Python script

-   inventory - contains the inventory Python script that will generate human
    readable CSV files

-   data - location where extracted JSON data and output CSVs will be stored

-   sampledata - contains pre-generated sample files
-   [JMESPath.py](https://github.com/jmespath/jmespath.py) library for JSON
    processing in Python

-   Admin or Co-admin rights to the subscription you want to extract information
    from.

### Extraction on Windows 

To run the PowerShell scripts on Windows, simply open PowerShell and navigate to
the **samplecode\\extract\\windows** folder and run:

>   .\\extract.ps1 \<Subscripton ID\>

The script will ask you to login two times: once for ARM mode and again for ASM
mode. On completion, several files will be generated with the VM and storage
account information for the subscription you specified. These files will be
stored in the **samplecode\\data\\\<Subscription ID\>** folder.

### Extraction on Linux

Before running the extraction script, you need to login to the Azure CLI apps.
In CLI 2.0 you can log on to a subscription using:

>   az login

In CLI 1.0, you can log on to a subscription using:

>   azure login

Once both are logged in navigate to the **samplecode/extract/linux** folder and
run:

>   bash extract.sh \<Subscripton ID\>

On completion, several files will be generated with the VM and storage account
information for the subscription you specified. These files will be stored in
the **samplecode/data/\<Subscription ID\>** folder.

### Transform

Navigate to the folder **samplecode/transform** and run:

>   python transform.py \<Subscripton ID\>

This will load the data from the specified subscription and generate a combined
**transformeddata.json** file in the **samplecode/data/\<Subscription ID\>**
folder.

### Inventory

Navigate to the folder **samplecode/inventory** and run:

>   python inventory.py \<Subscripton ID\>

This will load the **transformeddata.json** file and generate two CSV files in
the **samplecode/data/\<Subscription ID\>** folder:

-   vmInventory.csv - a list of VMs and information about them

-   storageAccountInventory.csv - a list of all storage drives used by the VMs

## MSFT OSS Code Of Conduct Notice

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
