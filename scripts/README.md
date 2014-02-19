## Processing Scripts

The process is broken into three phases: 

1. Download and unzip
2. Process XML
3. Post-processing for API and other outputs 

#### Requirements

- Python 2.6+ 
- [PIP](http://www.pip-installer.org/en/latest/installing.html#install-or-upgrade-pip)
- `pip install requirements.txt` 
- unzip (if not on OSX)
- wget (if not on Ubuntu)
- 30+GB of free space 

#### 1. Download and Unzip 
The download and unzip script will download 16GB from DailyMed and unzip into temporary folders. 

To run: 

```
cd pillbox-data-process
cd scripts
./download.sh
./unzip.sh
```

#### 2. Process XML

After the downloading is finished, to process the unzipped XML files, run `master.py`. This script will the following files: `xpath.py`, `rxnorm.py`, `errors.py`, and `makecsv.py`. 

To run: 

```
./master.py 
```

#### 3. Post-processing

To run any post-processing on the generated CSV or json files, run `api.py` or generate an additional script. 

To run: 

```
./api.py
```