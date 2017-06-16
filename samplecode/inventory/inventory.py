#!/usr/bin/env python

import sys
import os
import json
import importlib
import importlib.util
import datetime

if len(sys.argv) > 1:
    subscriptionId = sys.argv[1]
elif len(sys.argv) == 1:
    subscriptionId = input("Enter subscriptionId: ")
    

print("Analysis started at: ", datetime.datetime.now())

pathname = os.path.dirname(sys.argv[0])
scriptFilePath = os.path.abspath(pathname)

dataFilePath = os.path.join(scriptFilePath, "../data/", subscriptionId)
standardizedFile = open(dataFilePath + "/transformeddata.json", "r")
standardardizedJson = json.load(standardizedFile)

#Load all the rules configured in rulesconfig.json 
ruleConfigFilePath = os.path.join(scriptFilePath, "rulesconfig.json")
ruleConfigFile = open(ruleConfigFilePath, "r")
ruleConfigJson = json.load(ruleConfigFile)

modulesPath = os.path.join(scriptFilePath,"rules")

analysisRuleModules = []
analysisOutputJson = json.loads('{"analysisOutput" : {}}')

analysisOutput = analysisOutputJson["analysisOutput"]

for rule in ruleConfigJson["rules"]:
    ruleName = rule["ruleName"]
    ruleType = rule["ruleType"]
    moduleFilePath = os.path.join(modulesPath, rule["moduleFilePath"])
    moduleName = moduleFilePath.split(".")[0]

    spec = importlib.util.spec_from_file_location(moduleName, moduleFilePath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    analysisRuleModules.append((ruleName, ruleType, module))
    analysisOutput[ruleName] = None

#Execute analysis rules
for rule in analysisRuleModules:
    ruleName = rule[0]
    ruleType = rule[1]
    ruleModule = rule[2]

    ruleOutput = ruleModule.executeRule(standardardizedJson)
    outputFile = open(dataFilePath + "/" + ruleName + ".csv", "w")
    outputFile.write(ruleOutput )


print("Analysis completed at: ", datetime.datetime.now())
