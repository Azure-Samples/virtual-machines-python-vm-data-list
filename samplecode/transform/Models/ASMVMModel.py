import json
import jmespath

class CLIVM(object):
    def __init__(self,cliVM):
        availSet = {}
        availSet["id"] = jmespath.search('AvailabilitySetName',cliVM)
        availSet["resourceGroup"] = None
        self.availabilitySet = availSet
        
        bootDiagnostics = {}
        bootDiagnostics['enabled'] = jmespath.search('DebugSettings.BootDiagnosticsEnabled',cliVM)
        bootDiagnostics['storageUri'] = None        
        bootDiagnostics['ConsoleScreenshotBlobUri'] = jmespath.search('DebugSettings.ConsoleScreenshotBlobUri',cliVM)
        self.diagnosticsProfile = bootDiagnostics

        hardwareProfile = {}
        hardwareProfile['vmSize'] = jmespath.search('InstanceSize',cliVM)
        self.hardwareProfile = hardwareProfile

        self.id = None
        self.instanceView = None
        self.licenseType = None
        self.location = jmespath.search('Location',cliVM)
        self.name = jmespath.search('VMName',cliVM)
        
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
        self.provisioningState = jmespath.search('InstanceStatus',cliVM)
        self.resourceGroup = None

        resources = []
        resource = {}
        resource['autoUpgradeMinorVersion'] = None
        resource['forceUpdateTag'] = None
        resource['id'] = None
        resource['instanceView'] = None
        resource['location'] = None
        resource['name'] = None
        resource['protectedSettings'] = None
        resource['provisioningState'] = jmespath.search('InstanceStatus',cliVM)
        resource['publisher'] = None
        resource['resourceGroup'] = None
        resource['tags'] = None
        resource['type'] = None
        resource['typeHandlerVersion'] = None
        resource['virtualMachineExtensionType'] = None
        settings = {}
        settings['SequenceVersion'] = None
        settings['KeyVaultURL'] = None
        settings['AADClientID'] = None
        settings['KeyEncryptionKeyURL'] = None
        settings['EncryptionOperation'] = None
        settings['AADClientCertThumbprint'] = None
        settings['KeyEncryptionKeyURL'] = None
        settings['VolumeType'] = None
        settings['KeyEncryptionAlgorithm'] = None
        resource['settings'] = settings
        resources.append(resource)
        self.resources = resources

        storageProfile = {}
        dataDisks = []
        cliDataDisks = jmespath.search('DataDisks',cliVM)
        for item in cliDataDisks:
            dataDisk = {}
            dataDisk['caching'] = jmespath.search('hostCaching',item)
            dataDisk['diskLabel'] = None
            dataDisk['name'] = jmespath.search('name',item)
            dataDisk['lun'] = None
            dataDisk['createOption'] = None
            dataDisk['image'] = None
            dataDisk['diskSizeGb'] = jmespath.search('logicalDiskSizeInGB',item)
           #dataDisk['mediaLink'] = jmespath.search('mediaLink',item)
            vhd = {}
            vhd['uri'] = jmespath.search('MediaLink',item)
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
        osDisk['caching'] = jmespath.search('OSDisk.hostCaching',cliVM)
        osDisk['createOption'] = None
        osDisk['diskSizeGb'] = None
        osDisk['encryptionSettings'] = None
        osDisk['image'] = jmespath.search('OSDisk.sourceImageName',cliVM)
        osDisk['name'] = jmespath.search('OSDisk.name',cliVM)
        osDisk['mediaLink'] = jmespath.search('OSDisk.mediaLink',cliVM)
        osDisk['operatingSystem'] = jmespath.search('OSDisk.operatingSystem',cliVM)
        osDisk['iOType'] = jmespath.search('OSDisk.iOType',cliVM)
        osDisk['osType'] = jmespath.search('OSDisk.operatingSystem',cliVM)
        osDisk['diskLabel'] = None
        osDisk['resizedSizeInGB'] = None
        osDisk['extensionData'] = None
        vhd = {}
        vhd['uri'] = jmespath.search('OSDisk.mediaLink',cliVM)
        osDisk['vhd'] = vhd
        storageProfile['osDisk'] = osDisk
        self.storageProfile = storageProfile

        self.tags = None
        self.type = 'Microsoft.Compute/virtualMachines'
        self.vmId = None
        self.dnsName = jmespath.search('DNSName',cliVM)
        self.ipAddress = jmespath.search('IPAddress',cliVM)
        self.image = jmespath.search('Image',cliVM)
        self.reservedIPName = jmespath.search('ReservedIPName',cliVM)
        
       
        virtualIPAddresses = []
        vipAddresses = jmespath.search('VirtualIPAddresses',cliVM)
        for vip in vipAddresses:    
            virtualIPAddress = {}
            virtualIPAddress['address'] = jmespath.search('address',vip)
            virtualIPAddress['isDnsProgrammed'] = jmespath.search('isDnsProgrammed',vip)
            virtualIPAddress['name'] = jmespath.search('name',vip)
            virtualIPAddresses.append(virtualIPAddress)
        self.virtualIPAddresses = virtualIPAddresses

        network = {}
        endpoints = []
        cliEndpoints = jmespath.search('Network.Endpoints',cliVM)
        for item in cliEndpoints:
            endpoint = {}
            endpoint['localPort'] = jmespath.search('localPort',item)
            endpoint['name'] = jmespath.search('name',item)
            endpoint['port'] = jmespath.search('port',item)
            endpoint['protocol'] = jmespath.search('protocol',item)
            endpoint['virtualIPAddress'] = jmespath.search('virtualIPAddress',item)
            endpoint['enableDirectServerReturn'] = jmespath.search('enableDirectServerReturn',item)
            endpoint['loadBalancedEndpointSetName'] = jmespath.search('loadBalancedEndpointSetName',item)            
            loadBalancerProbe = {}
            loadBalancerProbe['path'] = jmespath.search('loadBalancerProbe.path',item)
            loadBalancerProbe['port'] = jmespath.search('loadBalancerProbe.port',item)
            loadBalancerProbe['protocol'] = jmespath.search('loadBalancerProbe.protocol',item)
            loadBalancerProbe['intervalInSeconds'] = jmespath.search('loadBalancerProbe.intervalInSeconds',item)
            loadBalancerProbe['timeoutInSeconds'] = jmespath.search('loadBalancerProbe.timeoutInSeconds',item)
            loadBalancerProbe['extensionData'] = None
            endpoint['loadBalancerProbe'] = loadBalancerProbe
            endpoint['endpointAccessControlList'] = None
            endpoint['loadBalancerName'] = None
            endpoint['idleTimeoutInMinutes'] = None
            endpoint['loadBalancerDistribution'] = None
            endpoint['virtualIPName'] = None
            endpoint['extensionData'] = None
            endpoints.append(endpoint)
        network['endpoints'] = endpoints
        network['virtualIPGroups'] = None
        network['staticVirtualNetworkIPAddress'] = None
        network['networkSecurityGroup'] = None
        network['publicIPs'] = []
        network['networkInterfaces'] = []
        network['ipForwarding'] = None
        network['extensionData'] = None
        self.network = network       

        self.serviceName = jmespath.search('ServiceName',cliVM)    
        self.instanceStateDetails = None 
        self.powerState = None 
        self.instanceErrorCode = None 
        self.instanceFaultDomain = None 
        self.instanceName = jmespath.search('VMName',cliVM) 
        self.instanceUpgradeDomain = None 
        self.instanceSize = jmespath.search('InstanceSize',cliVM) 
        self.hostName = jmespath.search('VMName',cliVM)  
        self.publicIPName = None 
        self.publicIPDomainNameLabel = None 
        self.virtualNetworkName = None 
        self.remoteAccessCertificateThumbprint = None 

class PSVM(object):
    def __init__(self,cliVM):

        availSet = {}
        availSet["id"] = jmespath.search('VM.AvailabilitySetName',cliVM)
        availSet["resourceGroup"] = None
        self.availabilitySet = availSet
        
        bootDiagnostics = {}
        bootDiagnostics['enabled'] = jmespath.search('VM.DebugSettings.BootDiagnosticsEnabled',cliVM)
        bootDiagnostics['storageUri'] = None
        bootDiagnostics['ConsoleScreenshotBlobUri'] = jmespath.search('VM.DebugSettings.ConsoleScreenshotBlobUri',cliVM)
        self.diagnosticsProfile = bootDiagnostics

        hardwareProfile = {}
        hardwareProfile['vmSize'] = jmespath.search('InstanceSize',cliVM)
        self.hardwareProfile = hardwareProfile

        self.id = None
        self.instanceView = None
        self.licenseType = None
        self.location = jmespath.search('Location',cliVM)
        self.name = jmespath.search('VMName',cliVM)
        
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
        self.provisioningState = jmespath.search('InstanceStatus',cliVM)
        self.resourceGroup = None

        resources = []
        resource = {}
        resource['autoUpgradeMinorVersion'] = None
        resource['forceUpdateTag'] = None
        resource['id'] = None
        resource['instanceView'] = None
        resource['location'] = None
        resource['name'] = None
        resource['protectedSettings'] = None
        resource['provisioningState'] = jmespath.search('InstanceStatus',cliVM)
        resource['publisher'] = None
        resource['resourceGroup'] = None
        resource['tags'] = None
        resource['type'] = None
        resource['typeHandlerVersion'] = None
        resource['virtualMachineExtensionType'] = None
        settings = {}
        settings['SequenceVersion'] = None
        settings['KeyVaultURL'] = None
        settings['AADClientID'] = None
        settings['KeyEncryptionKeyURL'] = None
        settings['EncryptionOperation'] = None
        settings['AADClientCertThumbprint'] = None
        settings['KeyEncryptionKeyURL'] = None
        settings['VolumeType'] = None
        settings['KeyEncryptionAlgorithm'] = None
        resource['settings'] = settings
        resources.append(resource)
        self.resources = resources

        storageProfile = {}
        dataDisks = []
        cliDataDisks = jmespath.search('VM.DataVirtualHardDisks',cliVM)
        for item in cliDataDisks:
            dataDisk = {}
            dataDisk['caching'] = jmespath.search('HostCaching',item)
            dataDisk['diskLabel'] = jmespath.search('DiskLabel',item)
            dataDisk['createOption'] = None
            dataDisk['image'] = None
            dataDisk['name'] = jmespath.search('DiskName',item)
            dataDisk['lun'] = jmespath.search('Lun',item)
            dataDisk['diskSizeGb'] = jmespath.search('LogicalDiskSizeInGB',item)
            vhd = {}
            vhd['uri'] = jmespath.search('MediaLink',item)
            dataDisk['vhd'] = vhd
            dataDisk['sourceMediaLink'] = jmespath.search('SourceMediaLink',item)
            dataDisk['ioType'] = jmespath.search('IOType',item)
            dataDisk['extensionData'] = jmespath.search('ExtensionData',item)
            dataDisks.append(dataDisk)
        storageProfile['dataDisks'] = dataDisks

        imageReference = {}
        imageReference['offer'] = None
        imageReference['publisher'] = None
        imageReference['sku'] = None
        imageReference['version'] = None
        storageProfile['imageReference'] = imageReference

        osDisk = {}
        osDisk['caching'] = jmespath.search('VM.OSVirtualHardDisk.HostCaching',cliVM)
        osDisk['createOption'] = None
        osDisk['diskSizeGb'] = None
        osDisk['encryptionSettings'] = None
        osDisk['image'] = jmespath.search('VM.OSVirtualHardDisk.SourceImageName',cliVM)
        osDisk['name'] = jmespath.search('VM.OSVirtualHardDisk.DiskName',cliVM)
        osDisk['mediaLink'] = jmespath.search('VM.OSVirtualHardDisk.MediaLink',cliVM)
        osDisk['operatingSystem'] = jmespath.search('VM.OSVirtualHardDisk.OS',cliVM)
        osDisk['iOType'] = jmespath.search('VM.OSVirtualHardDisk.IOType',cliVM)
        osDisk['osType'] = jmespath.search('VM.OSVirtualHardDisk.OS',cliVM)
        osDisk['diskLabel'] = jmespath.search('VM.OSVirtualHardDisk.DiskLabel',cliVM)
        osDisk['resizedSizeInGB'] = jmespath.search('VM.OSVirtualHardDisk.ResizedSizeInGB',cliVM)
        osDisk['extensionData'] = jmespath.search('VM.OSVirtualHardDisk.ExtensionData',cliVM)
        vhd = {}
        vhd['uri'] = jmespath.search('VM.OSVirtualHardDisk.MediaLink',cliVM)
        osDisk['vhd'] = vhd
        storageProfile['osDisk'] = osDisk
        self.storageProfile = storageProfile

        self.tags = None
        self.type = 'Microsoft.Compute/virtualMachines'
        self.vmId = None
        self.dnsName = jmespath.search('DNSName',cliVM)
        self.ipAddress = jmespath.search('IPAddress',cliVM)
        self.image = jmespath.search('Image',cliVM)
        self.reservedIPName = jmespath.search('ReservedIPName',cliVM)
        
        vipAddresses = []
        virtualIPAddresses = []
        for vip in vipAddresses:    
            virtualIPAddress = {}
            virtualIPAddress['address'] = None
            virtualIPAddress['isDnsProgrammed'] = None
            virtualIPAddress['name'] = None
            virtualIPAddresses.append(virtualIPAddress)
        self.virtualIPAddresses = virtualIPAddresses

        network = {}
        endpoints = []

        psEndpoints = jmespath.search('VM.ConfigurationSets[0].InputEndpoints',cliVM)
        for item in psEndpoints:
            endpoint = {}
            endpoint['localPort'] = jmespath.search('LocalPort',item)
            endpoint['name'] = jmespath.search('Name',item)
            endpoint['port'] = jmespath.search('Port',item)
            endpoint['protocol'] = jmespath.search('Protocol',item)
            endpoint['virtualIPAddress'] = jmespath.search('Vip',item)
            endpoint['enableDirectServerReturn'] = jmespath.search('EnableDirectServerReturn',item)
            endpoint['loadBalancedEndpointSetName'] = jmespath.search('LoadBalancedEndpointSetName',item)
            loadBalancerProbe = {}
            loadBalancerProbe['path'] = jmespath.search('loadBalancerProbe.Path',item)
            loadBalancerProbe['port'] = jmespath.search('loadBalancerProbe.Port',item)
            loadBalancerProbe['protocol'] = jmespath.search('loadBalancerProbe.Protocol',item)
            loadBalancerProbe['intervalInSeconds'] = jmespath.search('loadBalancerProbe.PntervalInSeconds',item)
            loadBalancerProbe['timeoutInSeconds'] = jmespath.search('loadBalancerProbe.TimeoutInSeconds',item)
            loadBalancerProbe['extensionData'] = jmespath.search('loadBalancerProbe.ExtensionData',item)
            endpoint['loadBalancerProbe'] = loadBalancerProbe
            endpoint['loadBalancerProbe'] = loadBalancerProbe
            endpoint['endpointAccessControlList'] = jmespath.search('EndpointAccessControlList',item)
            endpoint['loadBalancerName'] = jmespath.search('LoadBalancerName',item)
            endpoint['idleTimeoutInMinutes'] = jmespath.search('IdleTimeoutInMinutes',item)
            endpoint['loadBalancerDistribution'] = jmespath.search('LoadBalancerDistribution',item)
            endpoint['virtualIPName'] = jmespath.search('VirtualIPName',item)
            endpoint['extensionData'] = jmespath.search('ExtensionData',item)
            endpoints.append(endpoint)
        network['endpoints'] = endpoints
        network['virtualIPGroups'] = jmespath.search('VM.ConfigurationSets.VirtualIPGroups',cliVM)
        network['staticVirtualNetworkIPAddress'] = jmespath.search('VM.ConfigurationSets.StaticVirtualNetworkIPAddress',cliVM)
        network['networkSecurityGroup'] = jmespath.search('VM.ConfigurationSets.NetworkSecurityGroup',cliVM)
        network['publicIPs'] = jmespath.search('VM.ConfigurationSets.PublicIPs',cliVM)
        network['networkInterfaces'] = jmespath.search('VM.ConfigurationSets.NetworkInterfaces',cliVM)
        network['ipForwarding'] = jmespath.search('VM.ConfigurationSets.IPForwarding',cliVM)
        network['extensionData'] = jmespath.search('VM.ConfigurationSets.ExtensionData',cliVM)
        self.network = network       

        self.serviceName = jmespath.search('ServiceName',cliVM)    
        self.instanceStateDetails = jmespath.search('InstanceStateDetails',cliVM)     
        self.powerState = jmespath.search('PowerState',cliVM)     
        self.instanceErrorCode = jmespath.search('InstanceErrorCode',cliVM)     
        self.instanceFaultDomain = jmespath.search('InstanceFaultDomain',cliVM)     
        self.instanceName = jmespath.search('InstanceName',cliVM)     
        self.instanceUpgradeDomain = jmespath.search('InstanceUpgradeDomain',cliVM)     
        self.instanceSize = jmespath.search('InstanceSize',cliVM)     
        self.hostName = jmespath.search('HostName',cliVM)     
        self.publicIPName = jmespath.search('PublicIPName',cliVM)     
        self.publicIPDomainNameLabel = jmespath.search('PublicIPDomainNameLabel',cliVM)     
        self.virtualNetworkName = jmespath.search('VirtualNetworkName',cliVM)     
        self.remoteAccessCertificateThumbprint = jmespath.search('RemoteAccessCertificateThumbprint',cliVM)     