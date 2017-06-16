#!/usr/bin/env python
'''
This script will be used to analyze the storage accounts in the Azure subscription
'''


import json
import jmespath


def main():
    '''
    Main function gets called if this script is executed from the command line
    '''
    print(__file__)

def getStorageAccountNamefromDiskURI(diskUri):
    storageAccountName = diskUri.split("/")[2].split(".")[0]
    return storageAccountName


def OSDiskAnalysis(standardardizedJson, resourceType, outputCSV):
    
    
    AzureVMs = jmespath.search( "subscriptions[0]." + resourceType + ".virtualMachines", standardardizedJson)
    TotalAzureVMs = len(AzureVMs)

    if(TotalAzureVMs):
        #Loop through VMs to get additional details
        for VM in AzureVMs:
            #Only process VMs that are successfully provisioned
            provisioningState = VM["provisioningState"]
            if (provisioningState == "Succeeded" or resourceType == "ASM"):
                OSDiskUri = jmespath.search("storageProfile.osDisk.vhd.uri", VM)
                OSDiskStorageAccountName = getStorageAccountNamefromDiskURI(OSDiskUri)                
                VM["osDiskStorageAccountName"] = OSDiskStorageAccountName
                
                VMAvailabilitySetName = str(VM["availabilitySet"]["id"])
                if (VMAvailabilitySetName != "None" and resourceType == "ARM"):
                    VMAvailabilitySetName = VMAvailabilitySetName.split("/")[8]
                
                #Determine if Standard or Basic VM
                VMSize = VM["hardwareProfile"]["vmSize"]

                if "Standard" in VMSize:
                    VM["vmType"] = "Standard"
                else:
                    VM["vmType"] = "Basic"

                DiskInfo = [str(OSDiskUri), str(OSDiskStorageAccountName), str(VM["instanceName"]), str(VMAvailabilitySetName), "OS Disk " + str(VMSize), resourceType]
                outputCSV += ",".join(DiskInfo) + "\n"

                dataDisks = jmespath.search("storageProfile.dataDisks", VM)
                
                if len(dataDisks):
                    for dataDisk in dataDisks:
                        dataDiskUri = jmespath.search("vhd.uri", dataDisk)
                            
                        DataDiskInfo = [str(dataDiskUri), getStorageAccountNamefromDiskURI(dataDiskUri), str(VM["instanceName"]),str(VMAvailabilitySetName),"Data Disk " + str(jmespath.search("diskSizeGb", dataDisk)) + " GB", resourceType]
                        outputCSV += ",".join(DataDiskInfo) + "\n"

        
        
        
        
    return outputCSV


def executeRule(standardardizedJson):
    '''
    This function gets called from the main Analyze program
    to execute the relevant rules for storage account analysis
    '''
    print("Generating storage resource list")
    outputCSV = "Disk URI,Storage Account,Associated VM,Associated Availability Set, Disk Type,Deployment Model\n"

    #Check if ARM exists, then do ARM analysis
    hasARM = jmespath.search("subscriptions[0].ARM", standardardizedJson)

    if hasARM:
        outputCSV = OSDiskAnalysis(standardardizedJson, "ARM", outputCSV)    

    #Check if ASM exists, then do ASM analysis
    hasASM = jmespath.search("subscriptions[0].ASM", standardardizedJson)

    if hasASM:
        outputCSV = OSDiskAnalysis(standardardizedJson, "ASM", outputCSV)



    return outputCSV

if __name__ == "__main__":
    main()
