## Pillbox Data Process

The Pillbox data process uses a series of Python and Shell scripts to download, unzip, and parse the XML data provided by DailyMed. The process is broken into three phases:

1. Download (`download.sh`) and unzip (`unzip.sh`)
2. Process XML (`master.py`, `xpath.py`, `rxnorm.py`, `error.py`, `makecsv.py`)
3. Post-processing for static API and other outputs

The scripts generate a series of directories under a `/tmp` folder. In addition, the `master.py` data process generates two main intermediate Pillbox outputs: `/processed/csv/spl_data.csv` & `/processed/json/`.

#### Requirements

- Python 2.6+
- [PIP](http://www.pip-installer.org/en/latest/installing.html#install-or-upgrade-pip)
- `pip install requirements.txt`
- unzip (if not on OSX)
- wget (if not on Ubuntu)
- 30+GB of free space

### Using the scripts

#### 1. Download and Unzip
The download and unzip script will download 16GB from DailyMed and unzip into temporary folders.

To run:

```
./download.sh
./unzip.sh
```

#### 2. Process XML

After the downloading is finished, to process the unzipped XML files, run `master.py`. This script will use the `xpath.py`, `rxnorm.py`, `errors.py`, and `makecsv.py` modules.

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
