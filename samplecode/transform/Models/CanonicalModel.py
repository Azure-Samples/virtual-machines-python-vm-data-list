import os
import json
import jmespath
from datetime import datetime
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

class StandardSchema(object):
    def __init__(self,armStorage,armVM,asmStorage,asmVM,outputFilePath,subscriptionId):
            self.version = "1.0"
            self.creationDate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + 'Z'
            asm = {}
            asm['virtualMachines'] = asmVM
            asm['storageAccounts'] = asmStorage            
            arm = {}
            arm['virtualMachines'] = armVM
            arm['storageAccounts'] = armStorage
            subscription = {}
            subscription['subscriptionId'] = subscriptionId
            subscription['subscriptionName'] = "<SubscriptionName>"
            subscription['ASM'] = asm
            subscription['ARM'] = arm
            subscriptions = []
            subscriptions.append(subscription)
            self.subscriptions = subscriptions
       
