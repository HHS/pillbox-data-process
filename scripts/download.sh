#! /bin/sh

set -e

STARTTIME=$(date +%s)
echo "processing..."
today=$(date +"%Y-%m-%d")

# make temp directories if do not exist
mkdir -p ../tmp
mkdir -p ../tmp/download
mkdir -p ../tmp/download/$today

tmpDIR=../tmp/
cd $tmpDIR

# Download all Dailymed files 
wget -O download/$today/dm_spl_release_human_rx_part1.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_rx_part1.zip
wget -O download/$today/dm_spl_release_human_rx_part2.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_rx_part2.zip
wget -O download/$today/dm_spl_release_human_otc_part1.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_otc_part1.zip
wget -O download/$today/dm_spl_release_human_otc_part2.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_otc_part2.zip
wget -O download/$today/dm_spl_release_human_otc_part3.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_otc_part3.zip
wget -O download/$today/dm_spl_release_homeopathic.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_homeopathic.zip
wget -O download/$today/dm_spl_release_animal.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_animal.zip
wget -O download/$today/dm_spl_release_remainder.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_remainder.zip

echo "Dailymed files downloaded."
echo "Downloading complete."
ENDTIME=$(date +%s)
TOTALTIME=$((($ENDTIME-$STARTTIME)/60))
echo "Processing took $TOTALTIME minutes to complete."
