if [ 'sudo kill -9 $(cat pid.txt)' ]
then
    echo Stopped server
    rm pid.txt
else
    echo Failed to stop server
fi
