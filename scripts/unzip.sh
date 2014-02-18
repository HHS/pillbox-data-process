#! /bin/sh

set -e

STARTTIME=$(date +%s)
echo "processing..."
today=$(date +"%Y-%m-%d")

# make temp directories if do not exist
mkdir -p ../tmp
mkdir -p ../tmp/tmp-original
mkdir -p ../tmp/tmp-unzipped
mkdir -p ../tmp/processed/json
mkdir -p ../tmp/processed/csv
mkdir -p ../tmp/errors

tmpDIR=../tmp/
cd $tmpDIR

# Removes old files
tmpOriginal=tmp-original/
cd $tmpOriginal
for f in *.zip;
do
	if [ -f $f ]; then
		rm $f
	fi
done
echo "removed /tmp-original files"

# Removes old files
tmpUnzipped=../tmp-unzipped/
cd $tmpUnzipped
for f in *.zip;
do
	if [ -f $f ]; then
		rm $f
	fi
done
echo "removed /tmp-unzipped files"

# unzips main files to get individual zipped files
ORIGNDATA=../tmp-original/
cd $ORIGNDATA

unzip -qj ../download/$today/dm_spl_release_human_rx_part1.zip
unzip -qj ../download/$today/dm_spl_release_human_rx_part2.zip
unzip -qj ../download/$today/dm_spl_release_human_otc_part1.zip
unzip -qj ../download/$today/dm_spl_release_human_otc_part2.zip
unzip -qj ../download/$today/dm_spl_release_human_otc_part3.zip
unzip -qj ../download/$today/dm_spl_release_homeopathic.zip
unzip -qj ../download/$today/dm_spl_release_animal.zip
unzip -qj ../download/$today/dm_spl_release_remainder.zip

echo "original files unzipped to /tmp-original"

# loop through all individual zipped files to unzip
FILES=*.zip
for f in $FILES
do 
	ID=$(zipinfo -1 $f "*.xml" | sed 's/....$//')
	unzip -Cqo $f "*.xml" -d ../tmp-unzipped
	image=$(zipinfo -t $f)
	if [ ${image:0:1} != 1 ]; then
		unzip -Cqo $f "*.j*" -d ../tmp-unzipped/$ID
	fi
done
echo "all files unzipped."
echo "processing complete."
ENDTIME=$(date +%s)
TOTALTIME=$((($ENDTIME-$STARTTIME)/60))
echo "Processing took $TOTALTIME minutes to complete."