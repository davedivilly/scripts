#!/bin/bash

# Global variables

hqapi_path=/usr2/ddivilly/HYPERIC/hqapi1-client-6.0.4/bin
HypericNP_SD=/usr2/ddivilly/HYPERIC/hqapi1-client-6.0.4/conf/client.properties
HypericNP_LV=/usr2/ddivilly/HYPERIC/hqapi1-client-6.0.4/conf/client.properties.1
version=2.9.7
SD_file=groups-for-switch-extracted_SD.xml
LV_file=hyperic-resources-extracted-LV.xml

# Function (1) gathers the XML files needed from HQAPI 

hyperic_files(){

echo -e "---------------------------------------------------------------"
echo -e "Run this script from ---- WEBMON05 ----------------------------"
echo -e "Gathering GROUPS from Hyperic_SD  and Resources from HYPERIC_LV"
echo -e "---------------------------------------------------------------"

sleep 3

$hqapi_path/hqapi.sh resource list --prototype="SpringSource tc Runtime 7.0" --properties=$HypericNP_LV > /usr2/ddivilly/HYPERIC/hyperic-resources-extracted-LV.xml
$hqapi_path/hqapi.sh group list --properties=$HypericNP_SD > /usr2/ddivilly/HYPERIC/groups-for-switch-extracted_SD.xml

}

# Function (2) replaces Resource id="xxxxx" in SD Group  file with same value in LV Resource file # 

resource_id(){

echo -e "-----------------------------------------------------------------------------------"
echo -e "Replacing Resource id="xxxxx" in SD Group  file with same value in LV Resource file"
echo -e "-----------------------------------------------------------------------------------"

sleep 3

   while read line; do
    if [[ $line == *"Resource id"* ]] && [[ $line == *"Runtime"* ]] && [[ $line != "*Prototype*" ]] && [[ $line == *switch* ]]
    then
    id=$(echo "$line" | awk -F\" '{print $2}') 				# outputs ID from LV file #
    container=$(echo "$line" | awk -F\" '{print $4}') 			# outputs container name from LV file#
    id2=$(cat $SD_file | grep "$container" | awk -F'"' '{print$2}' | uniq ) 	# outputs ID from SD file # 
    if [ ! -z "$id2" ]; then                                            #if id not equal to null#
    sed -i "s/$id2/$id/" $SD_file					# swaps LV:ID with SD:ID and writes to group file
    fi
  fi
 done < $LV_file
}

# Function (3) removes id="xxxxx" in Role XML tag in SD Group file, otherwise sync will fail with this attribute #

role_id(){

echo -e "--------------------------------------------------------------------------------------------------"
echo -e "Removing id="xxxxx" in Role XML tag in SD Group file, otherwise sync will fail with this attribute"
echo -e "--------------------------------------------------------------------------------------------------"

sleep 3

 while read sd_line; do                                              

  if [[ $sd_line == *"Role id"* ]]; then
    role=$(echo $sd_line | awk -F' ' '{print $2}')
    sed -i "s/$role //" $SD_file
  fi

 done < $SD_file
}

# Function (4) Removes non-switch Resources to allow group sync #

resource_cleanup(){

echo -e "-----------------------------------------------------"
echo -e "Removing the non-switch resources to allow group sync"
echo -e "-----------------------------------------------------"

sleep 3

while read line; do
 if [[ $line == *"Resource id"* ]] && [[ $line == *"Runtime"* ]] && [[ $line != *Prototype* ]] && [[ $line != *switch* ]]
 then
   string="$(echo $line | awk -F\" '{print $4}')"
   #echo $string   
   sed -i "/$string/d" $SD_file  
 fi

done < $SD_file

}

# Function (5) Syncs modified Group XML file into Hyperic LV #

hyperic_sync() {

echo -e "---------------------------------------------"
echo -e "Syncing modified Group XML file to HYPERIC_LV"
echo -e "---------------------------------------------"

sleep 3

$hqapi_path/hqapi.sh group sync --batchSize 5 --properties=$HypericNP_LV --file=/usr2/ddivilly/HYPERIC/groups-for-switch-extracted_SD.xml

}

# Call functions 
hyperic_files
resource_id
role_id
resource_cleanup
hyperic_sync

exit 0

