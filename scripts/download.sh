#! /bin/sh

set -e

STARTTIME=$(date +%s)
echo "processing..."
today=$(date +"%Y-%m-%d")

# make temp directories if do not exist
mkdir -p ../tmp
mkdir -p ../tmp/download
mkdir -p ../tmp/tmp-original
mkdir -p ../tmp/tmp-unzipped
mkdir -p ../tmp/processed
mkdir -p ../tmp/processed/csv
mkdir -p ../tmp/errors

tmpDIR=../tmp/
cd $tmpDIR

# remove old files
if [ -f "download/original.zip" ]; then
	rm download/original.zip
fi
echo "removed original download"

tmpOriginal=tmp-original/
cd $tmpOriginal
for f in *.zip;
do
	if [ -f $f ]; then
		rm $f
	fi
done
echo "removed /tmp-original files"

tmpUnzipped=../tmp-unzipped/
cd $tmpUnzipped
for f in *.zip;
do
	if [ -f $f ]; then
		rm $f
	fi
done
echo "removed /tmp-unzipped files"

# will add download command here 
# for now, copy already downloaded file
cd ../
wget -O download/dm_spl_release_human_rx_part1.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_rx_part1.zip
wget -O download/dm_spl_release_human_rx_part2.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_rx_part2.zip
wget -O download/dm_spl_release_human_otc_part1.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_otc_part1.zip
wget -O download/dm_spl_release_human_otc_part2.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_otc_part2.zip
wget -O download/dm_spl_release_human_otc_part3.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_otc_part3.zip
wget -O download/dm_spl_release_homeopathic.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_homeopathic.zip
wget -O download/dm_spl_release_animal.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_animal.zip
wget -O download/dm_spl_release_remainder.zip ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_remainder.zip
echo "Dailymed files downloaded"

# unzips main files to get individual zipped files
ORIGNDATA=tmp-original/
cd $ORIGNDATA

unzip -qj ../download/dm_spl_release_human_rx_part1.zip
unzip -qj ../download/dm_spl_release_human_rx_part2.zip
unzip -qj ../download/dm_spl_release_human_otc_part1.zip
unzip -qj ../download/dm_spl_release_human_otc_part2.zip
unzip -qj ../download/dm_spl_release_human_otc_part3.zip
unzip -qj ../download/dm_spl_release_homeopathic.zip
unzip -qj ../download/dm_spl_release_animal.zip
unzip -qj ../download/dm_spl_release_remainder.zip

echo "original file unzipped to /tmp-original"

# loop through all individual zipped files to unzip
FILES=*.zip
for f in $FILES
do 
	ID=$(zipinfo -1 $f "*.xml" | sed 's/....$//')
	unzip -Cqo $f "*.xml" -d ../tmp-unzipped
	unzip -Cqo $f "*.jpg" -d ../tmp-unzipped/$ID
done
echo "all files unzipped."
echo "processing complete."
# now all original XML files are located in the /tmp-original/[today's date] folder
ENDTIME=$(date +%s)
TOTALTIME=$((($ENDTIME-$STARTTIME)/60))
echo "Processing took $TOTALTIME minutes to complete."
