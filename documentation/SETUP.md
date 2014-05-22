## Setting up your local environment

#### Setting up on Ubuntu

1. To set up on clean Ubuntu installation, run the following commands to intall the necessary requirements:

	```
	apt-get update
	apt-get install git -y
	apt-get install unzip -y
	sudo apt-get install python-setuptools python-dev build-essential -y
	apt-get install libxml2-dev -y
	apt-get install libxslt1-dev -y
	easy_install -U setuptools
	apt-get install python-pip
	pip install lxml
	pip install requests
	```

2. Clone this repo locally using the `git clone` command. This requires a Github account.
   ```
   git clone git@github.com:HHS/pillbox-data-process.git
   ```

3. Follow [steps for data process](https://github.com/HHS/pillbox-data-process/blob/updates/scripts/README.md).

#### Setting up on Mac OSX

Latest versions of OSX come with Python 2.7 installed. To run the Pillbox process, additional packages need to be installed. This assumes [Xcode](https://developer.apple.com/xcode/downloads/) & command line tools are installed. If not, install Xcode first.

1. Install pip
	```
	sudo easy_install pip
	```

2. Clone this repo locally using `git clone`. This requires a Github account.

	```
	git clone git@github.com:HHS/pillbox-data-process.git
	```

3. Install Python requirements for Pillbox
	```
	cd pillbox-data-process
	cd scripts
	sudo pip install -r requirements.txt
	```

4. Follow [steps for data process](https://github.com/HHS/pillbox-data-process/blob/updates/scripts/README.md).
