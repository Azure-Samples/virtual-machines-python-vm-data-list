#!/bin/bash

# This tool will be used to connect to an Azure subscription
# and collect data related to the storage accounts
# and virtual machines on the subscription for further analysis

# The output from this tool will be generated in the data/<subscriptionId> folder
# Multiple json files containing details of the VM and storage account in the subscription will be created
# Note: this script relies on the jq JSON processor.

echo -e "Before running this script, please login to your subscription using #azure login command. Open the URL : https://aka.ms/devicelogin in browser and enter the arbitary code \n"
SubscriptionId=$1
SnapshotDate=`date -u +"%FT%T.000Z"`
echo -e "Data extraction started at: $SnapshotDate \n"
# Data extraction tool start
#Check if SubscriptionID has been added
while [ "$SubscriptionId" = "" ]; do
     echo -e "Please enter the Azure Subscription ID or Q to quit"
     read SubscriptionId
       if [[ $SubscriptionId = "q" ]] || [[ $SubscriptionId = "Q" ]]
        then exit
       fi
done
#echo -e "Collecting information from subscription: $SubscriptionId \n"
echo -e "Setting Current Context to the Subscription"
az account set --subscription $SubscriptionId
echo "Setting asm mode"
azure config mode asm
# Create a new data folder for the subscription
mkdir -p  ../../data/$SubscriptionId
# Extract ARM Data using CLI 2.0"
echo -e "Gathering Virtual Machine details in ARM... \n"
az vm list > ../../data/$SubscriptionId/armclivm.json
echo -e "Gathering Storage Account details in ARM... \n"
az storage account list > ../../data/$SubscriptionId/armclisa.json
# Extract ASM Data
echo -e "Gathering Virtual Machine details in ASM... \n"
azure vm list --subscription $SubscriptionId --json > ../../data/$SubscriptionId/asmvm.json
azure vm list --subscription $SubscriptionId | head -n -1 |sed 1,4d |awk '{print $6}' > ../../data/$SubscriptionId/asmdnsname
if [ -s ../../data/$SubscriptionId/asmdnsname ]
then
IFS='
'
i=0
for asmdnsname in `cat ../../data/$SubscriptionId/asmdnsname`;
do
ServiceName=`echo $asmdnsname |sed 's/.*: //g;s/"//g'  | awk -F. '{print $1}'`
AvailabilitySetName=`azure service show --serviceName $ServiceName --subscription $SubscriptionId --json |grep -i -m1 availabilitySetName |sed 's/.*: //g;s/,//g;s/^.\(.*\).$/\1/'`
jq '.['$i'] +{"AvailabilitySetName": "'$AvailabilitySetName'", "ServiceName": "'$ServiceName'"}' ../../data/$SubscriptionId/asmvm.json >> ../../data/$SubscriptionId/asmvmlist.json 
i=$i+1
done
fi
jq -s . ../../data/$SubscriptionId/asmvmlist.json > ../../data/$SubscriptionId/asmclivm.json
rm -f ../../data/$SubscriptionId/asmvm.json ../../data/$SubscriptionId/asmdnsname ../../data/$SubscriptionId/asmvmlist.json
echo -e "Gathering Storage Account details in ASM... \n"
azure storage account list --subscription $SubscriptionId --json > ../../data/$SubscriptionId/asmclisa.json
echo -e "Extracted data available in the following folder : ../../data/$SubscriptionId folder. \n"
echo -e "Data Extraction Completed at : `date -u +"%FT%T.000Z"` \n"

