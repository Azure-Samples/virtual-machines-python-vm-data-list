#!/bin/bash
# Starting Transform of Collected data for Subscription
# Data transformation tool start
SubscriptionId=$1
#Check if SubscriptionID has been added
while [ "$SubscriptionId" = "" ]; do
     echo -e "Please enter the Azure Subscription ID or Q to quit"
     read SubscriptionId
       if [[ $SubscriptionId = "q" ]] || [[ $SubscriptionId = "Q" ]]
        then exit
       fi
done
echo -e "Tranforming data collected from subscription: $SubscriptionId"
SnapshotDate=`date -u +"%FT%T.000Z"`
#SubscriptionName=`az account show --subscription $SubscriptionId |jq .name`
# Concatenating json files into standardized json
jq -s '{"version": "1.0", "creationDate": "'$SnapshotDate'", "subscriptions": [{"subscriptionId": "'$SubscriptionId'", "subscriptionName": "'$SubscriptionName'", "ARM": {"virtualMachines": .[0], "storageAccounts": .[1] }}]}' ../data/$SubscriptionId/armclivm.json ../data/$SubscriptionId/armclisa.json > ../data/$SubscriptionId/transformeddata.json
echo -e "Tranformation of Data completed and the file transformeddata.json is placed ../data/$SubscriptionId folder"
