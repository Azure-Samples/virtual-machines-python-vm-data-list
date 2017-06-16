import json
import jmespath

class PSVM(object):
    def __init__(self,psVM):
        availSet = {}
        availSet["id"] = jmespath.search('AvailabilitySetReference.Id',psVM) 
        availSet["resourceGroup"] = jmespath.search('ResourceGroupName',psVM)
        self.availabilitySet = availSet

        bootDiagnostics = {}
        bootDiagnostics['enabled'] = jmespath.search('DiagnosticsProfile.BootDiagnostics.Enabled',psVM)
        bootDiagnostics['storageUri'] = None
        bootDiagnostics['ConsoleScreenshotBlobUri'] = None
        self.diagnosticsProfile = bootDiagnostics

        hardwareProfile = {}
        hardwareProfile['vmSize'] = jmespath.search('HardwareProfile.VmSize',psVM)
        self.hardwareProfile = hardwareProfile

        self.id = jmespath.search('Id',psVM)
        self.instanceView = None
        self.licenseType = None
        self.location = jmespath.search('Location',psVM)
        self.name = jmespath.search('Name',psVM)

        networkProfile = {}
        networkInterfaces = []
        networkInterface = {}
        networkInterface['id'] = None
        networkInterface['primary'] = None
        networkInterface['resourceGroup'] = None
        networkInterfaces.append(networkInterface)
        networkProfile['networkInterfaces'] = networkInterfaces
        self.networkProfile = networkProfile

        osProfile = {}
        osProfile['adminPassword'] = None
        osProfile['adminUsername'] = None
        osProfile['computerName'] = None
        osProfile['customData'] = None
        osProfile['linuxConfiguration'] = None
        osProfile['secrets'] = None
        windowsConfiguration = {}
        windowsConfiguration['additionalUnattendContent'] = None
        windowsConfiguration['enableAutomaticUpdates'] = None
        windowsConfiguration['provisionVmAgent'] = None
        windowsConfiguration['timeZone'] = None
        windowsConfiguration['winRm'] = None
        osProfile['windowsConfiguration'] = windowsConfiguration
        self.osProfile = osProfile

        self.plan = None
        self.provisioningState = jmespath.search('ProvisioningState',psVM)
        self.resourceGroup = jmespath.search('ResourceGroupName',psVM)

        resources = []
        resource = {}
        resource['autoUpgradeMinorVersion'] = None
        resource['forceUpdateTag'] = None
        resource['id'] = None
        resource['instanceView'] = None
        resource['location'] = None
        resource['name'] = None
        resource['protectedSettings'] = None
        resource['provisioningState'] = jmespath.search('ProvisioningState',psVM)
        resource['publisher'] = None
        resource['resourceGroup'] = None
        resource['tags'] = None
        resource['type'] = None
        resource['typeHandlerVersion'] = None
        resource['virtualMachineExtensionType'] = None
        resources.append(resource)
        self.resources = resources

        storageProfile = {}
        dataDisks = []
        psDataDisks = jmespath.search('StorageProfile.DataDisks',psVM)
        for item in psDataDisks:
            dataDisk = {}
            dataDisk['caching'] = jmespath.search('Caching',item)
            dataDisk['createOption'] = jmespath.search('CreateOption',item)
            dataDisk['image'] = jmespath.search('Image',item)
            dataDisk['diskLabel'] = None
            dataDisk['name'] = jmespath.search('Name',item)
            dataDisk['lun'] = jmespath.search('Lun',item)
            dataDisk['diskSizeGb'] = jmespath.search('DiskSizeGB',item)
            vhd = {}
            vhd['uri'] = jmespath.search('Vhd.Uri',item)
            dataDisk['vhd'] = vhd
            dataDisk['sourceMediaLink'] = None
            dataDisk['ioType'] = jmespath.search('iOType',item)
            dataDisk['extensionData'] = None
            dataDisks.append(dataDisk)
        storageProfile['dataDisks'] = dataDisks

        imageReference = {}
        imageReference['offer'] = None
        imageReference['publisher'] = None
        imageReference['sku'] = None
        imageReference['version'] = None
        storageProfile['imageReference'] = imageReference

        osDisk = {}
        osDisk['caching'] = jmespath.search('StorageProfile.OsDisk.Caching',psVM)
        osDisk['createOption'] = None
        osDisk['diskSizeGb'] = None
        osDisk['encryptionSettings'] = None
        osDisk['image'] = jmespath.search('StorageProfile.OsDisk.Image',psVM)
        osDisk['name'] = jmespath.search('StorageProfile.OsDisk.Name',psVM)
        osDisk['mediaLink'] = jmespath.search('StorageProfile.OsDisk.mediaLink',psVM)
        osDisk['operatingSystem'] = jmespath.search('StorageProfile.OsDisk.operatingSystem',psVM)
        osDisk['iOType'] = jmespath.search('StorageProfile.OsDisk.iOType',psVM)
        osDisk['osType'] = jmespath.search('StorageProfile.OsDisk.OsType',psVM)
        osDisk['diskLabel'] = None
        osDisk['resizedSizeInGB'] = None
        osDisk['extensionData'] = None
        vhd = {}
        vhd['uri'] = jmespath.search('StorageProfile.OsDisk.Vhd.Uri',psVM)
        osDisk['vhd'] = vhd
        storageProfile['osDisk'] = osDisk
        self.storageProfile = storageProfile

        self.tags = None
        self.type = 'Microsoft.Compute/virtualMachines'
        self.vmId = None
        self.dnsName = jmespath.search('DNSName',psVM)
        self.ipAddress = jmespath.search('IPAddress',psVM)
        self.image = jmespath.search('Image',psVM)
        self.reservedIPName = jmespath.search('ReservedIPName',psVM)


        self.serviceName = jmespath.search('ServiceName',psVM)
        self.instanceStateDetails = None
        self.powerState = None
        self.instanceErrorCode = None
        self.instanceFaultDomain = None
        self.instanceName = jmespath.search('Name',psVM)
        self.instanceUpgradeDomain = None
        self.instanceSize = jmespath.search('HardwareProfile.VmSize',psVM)
        self.hostName = jmespath.search('Name',psVM)
        self.publicIPName = None
        self.publicIPDomainNameLabel = None
        self.virtualNetworkName = None
        self.remoteAccessCertificateThumbprint = None
