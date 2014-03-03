#! /bin/bash

set -e

STARTTIME=$(date +%s)
date=$1
if [ $date ]; then
	echo "processing..."
else
	echo "Error: no date entered with command (ex: 2014-02-24)"
	exit 1
fi

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
for FOLDER in HRX HOTC HOMEO ANIMAL REMAIN;
do
	if [ -d $FOLDER ]; then
		rm -r $FOLDER
	fi
done
echo "removed /tmp-original files"

# Removes old files
tmpUnzipped=../tmp-unzipped/
cd $tmpUnzipped
for FOLDER in HRX HOTC HOMEO ANIMAL REMAIN;
do
	if [ -d $FOLDER ]; then
		rm -r $FOLDER
	fi
done
echo "removed /tmp-unzipped files"

# Removes old files
tmpImages=../tmp-images/
cd $tmpImages
for FOLDER in HRX HOTC HOMEO ANIMAL REMAIN;
do
	if [ -d $FOLDER ]; then
		rm -r $FOLDER
	fi
done
echo "removed /tmp-images files"

# create tmp subfolders
mkdir -p ../tmp-original/HRX
mkdir -p ../tmp-original/HOTC
mkdir -p ../tmp-original/HOMEO
mkdir -p ../tmp-original/ANIMAL
mkdir -p ../tmp-original/REMAIN

mkdir -p ../tmp-unzipped/HRX
mkdir -p ../tmp-unzipped/HOTC
mkdir -p ../tmp-unzipped/HOMEO
mkdir -p ../tmp-unzipped/ANIMAL
mkdir -p ../tmp-unzipped/REMAIN

mkdir -p ../tmp-images/HRX
mkdir -p ../tmp-images/HOTC
mkdir -p ../tmp-images/HOMEO
mkdir -p ../tmp-images/ANIMAL
mkdir -p ../tmp-images/REMAIN

# unzips main files to get individual zipped files
ORIGNDATA=../tmp-original/
cd $ORIGNDATA

unzip -qj ../download/$date/dm_spl_release_human_rx_part1.zip -d HRX/
unzip -qj ../download/$date/dm_spl_release_human_rx_part2.zip -d HRX/
unzip -qj ../download/$date/dm_spl_release_human_otc_part1.zip -d HOTC/
unzip -qj ../download/$date/dm_spl_release_human_otc_part2.zip -d HOTC/
unzip -qj ../download/$date/dm_spl_release_human_otc_part3.zip -d HOTC/
unzip -qj ../download/$date/dm_spl_release_homeopathic.zip -d HOMEO/
unzip -qj ../download/$date/dm_spl_release_animal.zip -d ANIMAL/
unzip -qj ../download/$date/dm_spl_release_remainder.zip -d REMAIN/

echo "original files unzipped to /tmp-original"

# loop through all individual zipped files to unzip
for FOLDER in HRX HOTC HOMEO ANIMAL REMAIN;
do
	if [ -d $FOLDER ]; then
		for f in `ls "$FOLDER/"`;
		do
			ID=$(zipinfo -1 "$FOLDER/$f" "*.xml" | sed 's/....$//')
			unzip -Cqo "$FOLDER/$f" "*.xml" -d ../tmp-unzipped/$FOLDER/
			unzip -Cqo "$FOLDER/$f" -d ../tmp-images/$FOLDER/${ID}
			rm ../tmp-images/$FOLDER/${ID}/${ID}.xml
		done
	fi
done

echo "all files unzipped."
echo "processing complete."
ENDTIME=$(date +%s)
TOTALTIME=$((($ENDTIME-$STARTTIME)/60))
echo "Processing took $TOTALTIME minutes to complete."
