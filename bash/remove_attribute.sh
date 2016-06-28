#!/bin/bash

file=<some_file>.xml

echo -e "----------------------------------------------"
echo -e "Removing Attribute "xxxxx" in  XML tag in file"
echo -e "-----------------------------------------------"

# Replace *"Resource id"* , *"Role id"* & *"resourceId"*"id"* with required string for line.

sleep 3

 while read line; do

  if [[ $line == *"Resource id"* ]] || [[ $line == *"Role id"* ]]; then
    attr1=$(echo $sd_line | awk -F' ' '{print $2}')
    sed -i "s/$attr1 //" $file
        elif [[ $sd_line == *"resourceId"*"id"* ]]; then
        attr2=$(echo $line |  awk -F' ' '{print $3}')
        #echo $attr2
        sed -i "s/$attr2 //" $file
  fi

 done < $file
