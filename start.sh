sudo echo Running server in background
source .env/bin/activate
sudo nohup python api.py > /dev/null 2>&1 &
echo $! > pid.txt
deactivate
