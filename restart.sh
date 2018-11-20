ps -ef|grep "app.py"|grep -v grep |head -1|awk '{print $2}'|xargs kill -9
ps -ef|grep "app.py"|grep -v grep |head -1|awk '{print $2}'|xargs kill -9
echo "杀死app"
nohup /usr/local/bin/python3 /apps2/srv/instance/bdg-agent-be/app.py &>/dev/null &
echo "启动app"