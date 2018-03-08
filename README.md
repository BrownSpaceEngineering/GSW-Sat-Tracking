# Detailed guide in guide/index.html

You will be able to reference the guide through URL/api after you deploy the api to URL.

Alternatively, you can visit the help page [here](http://www.michaelmao.me/GSW-Sat-Tracking/) without deploying. 

# Deploy

## Supported Systems
The code supports any machine running:
* bash
* zsh

This means, most Linux and OS X systems would work fine.

## Installation Requirements

* **Python3**
* **pip**
* **virtualenv**
* **Internet access**

### Requirements Installation Guide

* **Python3** can be found in most package managers or manually installed [here](https://www.python.org/downloads/)
* **pip** can be found in most package managers or you can install it manually following [this guide](https://pip.pypa.io/en/stable/installing/).
* **virtualenv** can be installed through `sudo -H pip install virtualenv`

## Installation
Both installation and reinstallation is done by running `sh install.sh` under the cloned directory. Make sure you have the requirements installed. There will be a prompt if a virtual environment is already present under your directory.

## Issues
* Note that oh-my-zsh may not print out virtualenv header during development mode due to weird theme settings.  
***This is an up-stream issue that cannot be fixed here.***

# DEVELOP
Running `source dev` would enter into development mode, where you will enter into the virtual environment for development.

Run `deactivate` to exit the environment.
