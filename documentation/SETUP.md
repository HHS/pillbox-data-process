## Setting up your local environment

#### Setting up on Ubuntu

1. To set up on clean Ubuntu installation, run the following commands to intall the necessary requirements:

    ```
    apt-get update
    apt-get install git unzip python-setuptools python-dev build-essential libxml2-dev libxslt1-dev libz-dev setuptools python-pip -y
    ```

2. Clone this repo locally using the `git clone` command. This requires a Github account.

    ```
    git clone git@github.com:HHS/pillbox-data-process.git
    ```

3. Install Python requirements for Pillbox

    ```
    cd pillbox-data-process
    cd scripts
    sudo pip install -r requirements.txt
    ```

4. Follow [steps for data process](https://github.com/HHS/pillbox-data-process/tree/master/scripts#pillbox-data-process).

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

4. Follow [steps for data process](https://github.com/HHS/pillbox-data-process/tree/master/scripts#pillbox-data-process).
