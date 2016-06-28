#!/bin/bash

SD_file=<some_file>.xml

echo -e "----------------------------------------------"
echo -e "Removing Attribute "xxxxx" in  XML tag in file"
echo -e "-----------------------------------------------"

sleep 3

 while read sd_line; do

  if [[ $sd_line == *"Resource id"* ]] || [[ $sd_line == *"Role id"* ]]; then
    role=$(echo $sd_line | awk -F' ' '{print $2}')
    sed -i "s/$role //" $SD_file
        elif [[ $sd_line == *"resourceId"*"id"* ]]; then
        role2=$(echo $sd_line |  awk -F' ' '{print $3}')
        #echo $role2
        sed -i "s/$role2 //" $SD_file
  fi

 done < $SD_file
