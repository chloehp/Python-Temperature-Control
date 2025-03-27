LOGFILE="/home/user/startup.log"

sleep 3
cd /home/user
. env1/bin/activate                     # activate venv
sleep 3
cd ptc
echo "$(date): STARTUP" >> $LOGFILE     # print to startup log
python main.py                          # start python temperature control
