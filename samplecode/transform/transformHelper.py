import os
import json
import codecs
import jmespath
BUFSIZE = 4096
BOMLEN = len(codecs.BOM_UTF8)
from enum import Enum


class Mode(Enum):
    INVALID = 0
    ASM = 1
    ARM = 2

class FileType(Enum):
      CLISA = 1
      PSSA = 2
      CLIVM = 3
      PSVM = 4

validFilesARM = ['armpssa.json','armpsvm.json']
validFilesASM = ['asmpssa.json','asmpsvm.json','asmclisa.json','asmclivm.json']

def loadJson(file_path):
     jsonText = ""
     if file_path:
        with open(file_path, "r+b") as fp:
            chunk = fp.read(BUFSIZE)
            if chunk.startswith(codecs.BOM_UTF8):
                i = 0
                chunk = chunk[BOMLEN:]
                while chunk:
                    fp.seek(i)
                    fp.write(chunk)
                    i += len(chunk)
                    fp.seek(BOMLEN, os.SEEK_CUR)
                    chunk = fp.read(BUFSIZE)
                fp.seek(-BOMLEN, os.SEEK_CUR)
                fp.truncate()
        with open(file_path) as json_data:
            jsonText = json.load(json_data)
            return jsonText

def validateFile(fileName):
    if fileName.lower() in validFilesARM:
        return Mode.ARM
    elif fileName.lower() in validFilesASM:
        return Mode.ASM
    else:
        return Mode.INVALID

def getFileType(jsonObject,mode):
    fileType = None
    if mode == Mode.ARM:    
        if jmespath.search('[0].StorageAccountName',jsonObject):
            fileType = FileType.PSSA
        elif jmespath.search('[0].Name',jsonObject):
            fileType = FileType.PSVM
    elif mode == Mode.ASM:
         if jmespath.search('[0].StorageAccountName',jsonObject):
            fileType = FileType.PSSA
         elif jmespath.search('[0].extendedProperties',jsonObject) or jmespath.search('[0].uri',jsonObject):
            fileType = FileType.CLISA
         elif jmespath.search('[0].VMName',jsonObject):
            fileType = FileType.CLIVM            
         elif jmespath.search('[0].VM',jsonObject):
            fileType = FileType.PSVM 
    return fileType;
