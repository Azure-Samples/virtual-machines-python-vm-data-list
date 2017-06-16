param (
        [Parameter(Mandatory=$false)]
        $SubscriptionID
      )

<#Tool Description

This tool will be used to connect to an Azure subscription 
and collect data related to the storage accounts 
and virtual machines on the subscription for further analysis.

The output from this tool will be generated in the data/<subscriptionId> folder 
Multiple json files containing details of the VM and storage account in the subscription will be created

#>
$SnapShotDate = Get-Date

Write-Host ("Data extraction started at: " + $SnapShotDate + "`n")

function LogException
{
    $_ | Out-File ".\error.log" -Append

    write-host “Caught an exception:” -ForegroundColor Red 
    write-host “Exception Type: $($_.Exception.GetType().FullName)” -ForegroundColor Red 
    write-host “Exception Message: $($_.Exception.Message)” -ForegroundColor Red
}

#Data extraction tool start

#Check if SubscriptionID has been added
while ($SubscriptionID.length -eq 0)
{
    $SubscriptionID = Read-Host -Prompt "Please enter the Azure Subscription ID or Q to quit"
        
    if ($SubscriptionID -eq "Q")
    {
        return;
    }
}


try
{
    #Add azure subscription using both ASM and ARM so that we can run both types of commandlets for the same subscription
    Write-Host ("Login twice to Azure account - ASM mode and ARM mode")

    Add-AzureAccount -ErrorAction Stop
    Add-AzureRMAccount -ErrorAction Stop

    #Trim to remove user entry related errors
    $SubscriptionID = $SubscriptionID.Trim()

    Write-Host ("Collecting information from subscription: " + $SubscriptionID)

    $Subscription = Get-AzureSubscription -SubscriptionId $SubscriptionID

    Set-AzureRmContext -SubscriptionId $SubscriptionID
    Select-AzureSubscription -SubscriptionId $SubscriptionID -Current

    #Create a new data folder for the subscription
    $FilePath ="../../data/" + $SubscriptionID 
    New-Item  $FilePath -Type Directory -Force

    #Extract output of the commandlets to json files

    $ARMSAFilePath = $FilePath + "/armpssa.json" 
    $ARMVMFilePath = $FilePath + "/armpsvm.json" 
    $ASMSAFilePath = $FilePath + "/asmpssa.json" 
    $ASMVMFilePath = $FilePath + "/asmpsvm.json" 
    
    #Extract ARM data
    Write-Host ("Getting virtual machine details in ARM...")
    Get-AzureRmVM | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 -FilePath $ARMVMFilePath

    Write-Host ("Getting storage account details in ARM...")
    Get-AzureRmStorageAccount | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 -FilePath $ARMSAFilePath 

    #Extract ASM data
    Write-Host ("Getting virtual machine details in ASM...")
    Get-AzureVM | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 -FilePath $ASMVMFilePath 

    Write-Host ("Getting storage account details in ASM...")
    Get-AzureStorageAccount | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 -FilePath $ASMSAFilePath 
}
catch
{
    #Log exception
    LogException
}
finally
{
    $EndDate = Get-Date
    $OutfilePath = Resolve-Path $FilePath
    Write-Host ("Extracted data available in the following folder: " + $OutfilePath + "`n")
    Write-Host ("Data extraction completed at: " + $EndDate + "`n")
}