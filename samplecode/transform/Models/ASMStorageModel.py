import json
import jmespath

class CLIStorage(object):
    def __init__(self,cliStorage):
        self.accessTier = None
        self.creationTime = None
        self.customDomain = None
        self.encryption = None
        self.id = None
        self.kind = None
        self.lastGeoFailoverTime = None
        self.location = jmespath.search('properties.location',cliStorage)
        self.name = jmespath.search('name',cliStorage)

        primaryEndpoint = {}
        primaryEndpoint['blob'] = jmespath.search('properties.endpoints[0]',cliStorage)
        primaryEndpoint['file'] = jmespath.search('properties.endpoints[3]',cliStorage)
        primaryEndpoint['queue'] = jmespath.search('properties.endpoints[1]',cliStorage)
        primaryEndpoint['table'] = jmespath.search('properties.endpoints[2]',cliStorage)

        self.primaryEndpoints = primaryEndpoint
        self.primaryLocation = jmespath.search('properties.geoPrimaryRegion',cliStorage)
        self.provisioningState = None
        self.resourceGroup = jmespath.search('extendedProperties.ResourceGroup',cliStorage)
        self.secondaryEndpoints = None
        self.secondaryLocation = jmespath.search('properties.geoSecondaryRegion',cliStorage)
        sku = {}
        sku['name'] = None
        sku['tier'] = None
        self.sku = sku
        self.statusOfPrimary = jmespath.search('properties.statusOfGeoPrimaryRegion',cliStorage)
        self.statusOfSecondary = None
        self.tags = None
        self.type = None
        self.uri = jmespath.search('uri',cliStorage)
        self.description = jmespath.search('properties.description',cliStorage)
        self.label = jmespath.search('properties.label',cliStorage)
        self.status = jmespath.search('properties.status',cliStorage)
        self.accountType = jmespath.search('properties.accountType',cliStorage)
        self.affinityGroup = None
        self.migrationState = None
        
class PSStorage(object):
    def __init__(self,psStorage):
        self.accessTier = None
        self.creationTime = None
        self.customDomain = None
        self.encryption = None
        self.id = None
        self.kind = None
        self.lastGeoFailoverTime = None
        self.location = jmespath.search('Location',psStorage)
        self.name = jmespath.search('StorageAccountName',psStorage)

        primaryEndpoint = {}
        primaryEndpoint['blob'] = jmespath.search('Endpoints[0]',psStorage)
        primaryEndpoint['file'] = jmespath.search('Endpoints[3]',psStorage)
        primaryEndpoint['queue'] = jmespath.search('Endpoints[1]',psStorage)
        primaryEndpoint['table'] = jmespath.search('Endpoints[2]',psStorage)

        self.primaryEndpoints = primaryEndpoint
        self.primaryLocation = jmespath.search('GeoPrimaryLocation',psStorage)
        self.provisioningState = None
        self.resourceGroup = None
        self.secondaryEndpoints = None
        self.secondaryLocation = None
        sku = {}
        sku['name'] = None
        sku['tier'] = None
        self.sku = sku
        self.statusOfPrimary = jmespath.search('StatusOfPrimary',psStorage)
        self.statusOfSecondary = jmespath.search('StatusOfSecondary',psStorage)
        self.tags = None
        self.type = None
        self.uri = None
        self.description = jmespath.search('StorageAccountDescription',psStorage)
        self.label = jmespath.search('Label',psStorage)
        self.status = jmespath.search('StorageAccountStatus',psStorage)
        self.accountType = jmespath.search('AccountType',psStorage)
        self.affinityGroup = jmespath.search('AffinityGroup',psStorage)
        self.migrationState = jmespath.search('MigrationState',psStorage)


        

        