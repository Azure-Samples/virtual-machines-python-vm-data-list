import json
import jmespath

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
        primaryEndpoint['blob'] = jmespath.search('PrimaryEndpoints.Blob',psStorage)
        primaryEndpoint['file'] = jmespath.search('PrimaryEndpoints.File',psStorage)
        primaryEndpoint['queue'] = jmespath.search('PrimaryEndpoints.Queue',psStorage)
        primaryEndpoint['table'] = jmespath.search('PrimaryEndpoints.Table',psStorage)

        self.primaryEndpoints = primaryEndpoint
        self.primaryLocation = jmespath.search('PrimaryLocation',psStorage)
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
