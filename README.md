# TopoDownloader
https://nationalmap.gov/ustopo/

SETUP:
-Change "searchfilepath" to the location of your CSV download lists.
-Change "OUTPUTFILEPATH" to the location you would like the maps saved to.  By default folders are created for each state.

This python script downloads the free US Topo maps from a CSV list.  These CSV lists can be downloaded from this website: 

https://geonames.usgs.gov/apex/f?p=262:1:0

Each search from this website can be exported to CSV.

This script will read those lists from the "searchfilepath" file path specified in the script and download each map.

The script is written to only download the latest maps (['Version'] == 'Current') and only the states given in the name of the CSV file ('Primary_State'] == inputfilestatename).  Other states are listed in the CSV file as well since there is overlap accross state lines.