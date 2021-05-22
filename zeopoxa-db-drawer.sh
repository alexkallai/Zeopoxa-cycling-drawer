#!/bin/bash

#USAGE: ./zeopoxa-db-drawer.sh [DB FILE]
#default is Zeopoxa_cycling.db

#Input file name get stored
if [[ $1 = "" ]];
then 
  echo "USAGE: ./zeopoxa-db-drawer.sh [DB FILE]"
else DB=$1
fi


#extracting coordinates from LATLON_ARRAY from main table into the COORDINATES variable
COORDINATES=$(
sqlite3 $DB "SELECT LATLON_ARRAY FROM main_table" |

#removing the unneeded characters and lines, so it's essentially a CSV file
tr -s "]" "\n" | #replace ] with newline
tr -s "}" "\n" | #replace } with newline
tr -dc " [:digit:] [:space:] . , \n " | #delete all cahracters except those in quotes
sed 's/^,//' | #delete commas from beginning of line 
awk 'NF'  # delete empty lines
)
echo "$COORDINATES" > COORDINATES.csv

./draw.py COORDINATES.csv
