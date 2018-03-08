# Checks if already installed
if [ $(ls -a | grep .env 2>/dev/null) ]
then
    echo "Do you wish to reinstall?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) REINSTALL=1;break;;
            No ) exit;;
        esac
    done
fi

# Checks if python3 is installed
if [ $(command -v python3 2>/dev/null) ]
then
    PYTHON=$(command -v python3)
    echo "Using $PYTHON"
else
    echo "Please install Python3 and pip on Python3"
    exit
fi

# Checks if pip3 is installed
if [ $(command -v pip3 2>/dev/null) ]
then
    PIP=$(command -v pip3)
    echo "Using $PIP"
else
    echo "Please install pip on Python3"
    exit
fi

# Install virtualenv on python3 if not installed
if [ $($PIP freeze | grep virtualenv 2>/dev/null) ]
then
    # Purges past install if reinstall
    if [ "$REINSTALL" -eq 1 ]
    then
        sudo rm -rf .env
    fi
    
    echo virtualenv found
    virtualenv -p $PYTHON .env
    source .env/bin/activate
    pip install -r requirements.txt
    deactivate
else
    sudo -H $PIP install virtualenv
fi
