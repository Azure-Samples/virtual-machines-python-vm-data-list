import json
import jmespath

def main():
    print (__file__)

def getStorageAccountNamefromDiskURI(diskUri):
    storageAccountName = diskUri.split("/")[2].split(".")[0]
    return storageAccountName

def ARMVMAnalysis(standardizedJson, outputCSV):

    #ARM VM Analysis    
    #Has to be modified to support multiple subscriptions
    
    ARMVMs = jmespath.search( "subscriptions[0].ARM.virtualMachines[?provisioningState== 'Succeeded']", standardizedJson)
    TotalARMVMs = len(ARMVMs)

    if(TotalARMVMs):
        #Build output
        
        VMType = "ARM"
        #Loop through VMs to get additional details
        for VM in ARMVMs:
            
            OSDiskUri = jmespath.search("storageProfile.osDisk.vhd.uri", VM)
            OSDiskStorageAccountName = getStorageAccountNamefromDiskURI(OSDiskUri)
            VMName = VM["name"]
            VMRegion = VM["location"]
            VMResourceGroup = VM["resourceGroup"]
            VMAvailabilitySetName = str(VM["availabilitySet"]["id"])
            if VMAvailabilitySetName != "None":
                VMAvailabilitySetName = VMAvailabilitySetName.split("/")[8]
            VMSize= VM["instanceSize"]
            OSDiskStorageAccountName = getStorageAccountNamefromDiskURI(OSDiskUri)
            dataDisks = jmespath.search("storageProfile.dataDisks", VM)
            DataDiskCount = str(len(dataDisks))
            
            VMInfo = [str(VMName), str(VMType), str(VMRegion), str(VMResourceGroup), str(VMAvailabilitySetName), str(VMSize), str(OSDiskStorageAccountName), str(DataDiskCount)]
            outputCSV += ",".join(VMInfo)  + "\n"
        
        

    
    return outputCSV


def ASMVMAnalysis(standardizedJson, outputCSV):

    #ASM VM Analysis    
    #Has to be modified to support multiple subscriptions
    
    ASMVMs = jmespath.search( "subscriptions[0].ASM.virtualMachines", standardizedJson)
    TotalASMVMs = len(ASMVMs)

    if(TotalASMVMs):
        #Build output
        VMType = "ASM"

        #Loop through VMs to get additional details
        for VM in ASMVMs:
            
            OSDiskUri = jmespath.search("storageProfile.osDisk.vhd.uri", VM)
            OSDiskStorageAccountName = getStorageAccountNamefromDiskURI(OSDiskUri)
            VMName = VM["instanceName"]
            VMRegion = "N/A"
            VMResourceGroup = "N/A"
            VMAvailabilitySetName = str(VM["availabilitySet"]["id"])
            #if VMAvailabilitySetName != "None":
            #    VMAvailabilitySetName = VMAvailabilitySetName.split("/")[8]
            VMSize= VM["hardwareProfile"]["vmSize"]
            OSDiskStorageAccountName = getStorageAccountNamefromDiskURI(OSDiskUri)
            dataDisks = jmespath.search("storageProfile.dataDisks", VM)
            DataDiskCount = str(len(dataDisks))
            
            VMInfo = [str(VMName), str(VMType), str(VMRegion), str(VMResourceGroup), str(VMAvailabilitySetName), str(VMSize), str(OSDiskStorageAccountName), str(DataDiskCount)]
            outputCSV += ",".join(VMInfo)  + "\n"
        
        

    return outputCSV
    
def executeRule(standardizedJson):
    outputCSV = "VM Name,Type,Region,Resource Group,Availability Set,VM Size,OS Disk Storage Account, # of Data Disks"  + "\n"

    print("Executing VM analysis")

    hasARM = jmespath.search("subscriptions[0].ARM", standardizedJson)
    if hasARM:
        outputCSV = ARMVMAnalysis(standardizedJson, outputCSV)

    hasASM = jmespath.search("subscriptions[0].ASM", standardizedJson)

    if hasASM:
        outputCSV = ASMVMAnalysis(standardizedJson, outputCSV)

    return outputCSV

if __name__ == "__main__":
    main()
