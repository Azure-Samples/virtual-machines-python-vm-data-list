import os
import sys
import json
import jmespath
from Models import ASMStorageModel
from Models import ASMVMModel
from Models import ARMStorageModel
from Models import CanonicalModel
from Models import ARMVMModel
import transformHelper as Helper
import time
from os.path import basename
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

print(Fore.YELLOW + Style.BRIGHT + '**** JSON Schema Generator ****')
file_path = ''
storageAccountsASM = []
virtualMachinesASM = []
storageAccountsARM = []
virtualMachinesARM = []

def printError(msg):
    print(Fore.RED + Style.BRIGHT + msg)

def transformFile(fileType,item,mode):        
    if mode == Helper.Mode.ASM:
        if fileType == Helper.FileType.PSSA:
            storageAccountsASM.append(ASMStorageModel.PSStorage(item))
        elif fileType == Helper.FileType.CLISA:
            storageAccountsASM.append(ASMStorageModel.CLIStorage(item))
        elif fileType == Helper.FileType.CLIVM:
            virtualMachinesASM.append(ASMVMModel.CLIVM(item))
        elif fileType == Helper.FileType.PSVM:
            virtualMachinesASM.append(ASMVMModel.PSVM(item))
    elif mode == Helper.Mode.ARM:
        if fileType == Helper.FileType.PSSA:
            storageAccountsARM.append(ARMStorageModel.PSStorage(item))
        elif fileType == Helper.FileType.PSVM:
            virtualMachinesARM.append(ARMVMModel.PSVM(item))
       
    

def saveOutputFile(outputFileDir,storageAccountsASM,virtualMachinesASM,storageAccountsARM,virtualMachinesARM,subscriptionId):
    outputFilePath = outputFileDir
    if os.path.isdir(outputFileDir):
        outputFilePath = os.path.join(outputFileDir,'transformeddata.json')
    result = CanonicalModel.StandardSchema(storageAccountsARM,virtualMachinesARM,storageAccountsASM,virtualMachinesASM,outputFilePath,subscriptionId)
    with open(outputFilePath, 'w') as outfile:
        json_data = json.dump(result,outfile,default=lambda o: o.__dict__,sort_keys=True, indent=4)
    return outputFilePath

def GenerateTransformedOutput(inputFileDir,subscriptionId):
    directory = os.path.normpath(inputFileDir)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            mode = Helper.validateFile(file)
            if mode != Helper.Mode.INVALID:
                fileType = None
                f = open(os.path.join(subdir, file),'r')
                a = f.read()
                if a:
                    jsonObject = Helper.loadJson(os.path.join(inputFileDir,file))
                    if jmespath.search('[0]',jsonObject):
                        fileType = Helper.getFileType(jsonObject,mode)
                        for item in jsonObject:
                            transformFile(fileType,item,mode)
                    else:
                         if mode == Helper.Mode.ARM:
                            if jmespath.search('StorageAccountName',jsonObject):
                                storageAccountsARM.append(ARMStorageModel.PSStorage(jsonObject))
                            elif jmespath.search('Name',jsonObject):
                                virtualMachinesARM.append(ARMVMModel.PSVM(jsonObject))
                         elif mode == Helper.Mode.ASM:
                                if jmespath.search('StorageAccountName',jsonObject):
                                        storageAccountsASM.append(ASMStorageModel.PSStorage(jsonObject))      
                                elif jmespath.search('extendedProperties',jsonObject) or jmespath.search('uri',jsonObject):
                                        storageAccountsASM.append(ASMStorageModel.CLIStorage(jsonObject))
                                elif jmespath.search('VMName',jsonObject):
                                        virtualMachinesASM.append(ASMVMModel.CLIVM(jsonObject))            
                                elif jmespath.search('VM',jsonObject):
                                        virtualMachinesASM.append(ASMVMModel.PSVM(jsonObject))                 
                print("'" + file + "' file processed.")
                f.close()


    outputFilePath = saveOutputFile(inputFileDir,storageAccountsASM,virtualMachinesASM,storageAccountsARM,virtualMachinesARM,subscriptionId)
    print(Fore.GREEN + Style.BRIGHT + 'Canonical schema is created successfully. Path - "' + outputFilePath + '"')


def parameterValidation(inputFileDir,subscriptionId):
    isValid = True
    if not os.path.isdir(inputFileDir):        
        printError('Invalid input directory - ' + inputFileDir)
        isValid = False
    if not subscriptionId:
        printError('Subscription id is required.')
        isValid = False
    return isValid

def main(argv):  
    if len(sys.argv) > 1:
        subscriptionId = sys.argv[1]
    elif len(sys.argv) == 1:
        subscriptionId = input("Enter subscriptionId: ")
 
    if len(subscriptionId) >= 1:
        inputFileDir=''
        if len(argv) == 2:
            inputFileDir = argv[1]        
        if not inputFileDir:
            inputFileDir = os.path.abspath(__file__).rsplit('\\',2)[0] + "\\data\\" + subscriptionId         
        print('Input file(s) directory : ' + inputFileDir)
        print('subscription Id : ' + subscriptionId)
        if parameterValidation(inputFileDir,subscriptionId):
            GenerateTransformedOutput(inputFileDir,subscriptionId)
    else:
        printError('Provide all the parameters from command line argument. Example: <InputFilePath> <OutDir>')

# Pass command line arguments
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        printError("Error:" + str(e))