import os
import json
import jmespath
import transformHelper as Helper
from datetime import datetime
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

class StandardSchema(object):
    def __init__(self,asmStorage,asmVM,outputFilePath,subscriptionId):
        if(not os.path.exists(outputFilePath) or os.path.getsize(outputFilePath) == 0):
            self.version = "1.0"
            self.creationDate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + 'Z'
            asm = {}
            asm['virtualMachines'] = asmVM
            asm['storageAccounts'] = asmStorage
            subscription = {}
            subscription['subscriptionId'] = subscriptionId
            subscription['subscriptionName'] = "<SubscriptionName>"
            subscription['ASM'] = asm
            arm = {}
            arm['virtualMachines'] = []
            arm['storageAccounts'] = []
            subscription['ARM'] = arm
            subscriptions = []
            subscriptions.append(subscription)    
            self.subscriptions = subscriptions
        else:
            res = Helper.loadJson(outputFilePath)
            self.version = jmespath.search('version',res)
            self.creationDate = jmespath.search('creationDate',res)
            asm = {}
            vms = jmespath.search('subscriptions[0].ASM.virtualMachines',res)
            sas = jmespath.search('subscriptions[0].ASM.storageAccounts',res)            
            asmVMs = vms if vms else []
            asmSAs = sas if sas else []
            for vm in asmVM:
                asmVMs.append(vm)
            for sa in asmStorage:
                asmSAs.append(sa)
            asm['virtualMachines'] = asmVMs
            asm['storageAccounts'] = asmSAs
            subscription = {}
            subId = jmespath.search('subscriptions[0].subscriptionId',res)
            if subId:
                print(Fore.YELLOW + Style.BRIGHT + 'Previous subscription id(' + subId + ') is replaced with new subscription id(' + subscriptionId + ')')
            subscription['subscriptionId'] = subscriptionId
            subscription['subscriptionName'] = jmespath.search('subscriptions[0].subscriptionName',res)
            subscription['ASM'] = asm
            subscription['ARM'] = jmespath.search('subscriptions[0].ARM',res)
            subscriptions = []
            subscriptions.append(subscription)    
            self.subscriptions = subscriptions
            
        