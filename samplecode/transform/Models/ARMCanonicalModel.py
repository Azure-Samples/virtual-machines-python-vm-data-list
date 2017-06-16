import os
import json
import jmespath
import transformHelper as Helper
from datetime import datetime
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

class StandardSchema(object):
    def __init__(self,armStorage,armVM,outputFilePath,subscriptionId):
        if(not os.path.exists(outputFilePath) or os.path.getsize(outputFilePath) == 0):
            self.version = "1.0"
            self.creationDate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + 'Z'
            asm = {}
            asm['virtualMachines'] = []
            asm['storageAccounts'] = []            
            arm = {}
            arm['virtualMachines'] = [armVM]
            arm['storageAccounts'] = [armStorage]
            subscription = {}
            subscription['subscriptionId'] = subscriptionId
            subscription['subscriptionName'] = "<SubscriptionName>"
            subscription['ASM'] = asm
            subscription['ARM'] = arm
            subscriptions = []
            subscriptions.append(subscription)
            self.subscriptions = subscriptions
        else:
            res = Helper.loadJson(outputFilePath)
            self.version = jmespath.search('version',res)
            self.creationDate = jmespath.search('creationDate',res)
            arm = {}
            vms = jmespath.search('subscriptions[0].ARM.virtualMachines',res)
            sas = jmespath.search('subscriptions[0].ARM.storageAccounts',res)
            armVMs = vms if vms else []
            armSAs = sas if sas else []
            for vm in armVM:
                armVMs.append(vm)
            for sa in armStorage:
                armSAs.append(sa)
            arm['virtualMachines'] = armVMs
            arm['storageAccounts'] = armSAs
            subscription = {}
            subId = jmespath.search('subscriptions[0].subscriptionId',res)
            if subId:
                print(Fore.YELLOW + Style.BRIGHT + 'Previous subscription id(' + subId + ') is replaced with new subscription id(' + subscriptionId + ')')
            subscription['subscriptionId'] = subscriptionId
            subscription['subscriptionName'] = jmespath.search('subscriptions[0].subscriptionName',res)
            subscription['ARM'] = arm
            subscription['ASM'] = jmespath.search('subscriptions[0].ASM',res)
            subscriptions = []
            subscriptions.append(subscription)
            self.subscriptions = subscriptions
