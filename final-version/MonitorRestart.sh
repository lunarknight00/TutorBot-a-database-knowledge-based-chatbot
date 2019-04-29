#!/bin/sh
time=$(date "+%Y-%m-%d %H:%M:%S")
while true
do
	ps -ef | grep "python ./capstone-project-magnum-opus/final-version/comp9900_run.py" | grep -v "grep" > /dev/null 2>&1

if [ "$?" -eq 1 ]
then
	nohup python ./capstone-project-magnum-opus/final-version/comp9900_run.py > MainService.log 2>&1 &
	echo "[MS][${time}] Main service has restarted..."
fi

	ps -ef | grep "python ./capstone-project-magnum-opus/final-version/botapi.py" | grep -v "grep" > /dev/null 2>&1

if [ "$?" -eq 1 ]
then
	nohup python ./capstone-project-magnum-opus/final-version/botapi.py > BackendService.log 2>&1 &
	echo "[BS][${time}] Backend service has restarted..."
fi

	ps -ef | grep "elasticsearch" | grep -v "grep" > /dev/null 2>&1
if [ "$?" -eq 1 ]
then
	nohup ./elasticsearch-6.7.1/bin/elasticsearch > ESlog.log 2>&1 &
	echo "[ES][${time}] Elastic Search has restarted..."
fi

	ps -ef | grep "kibana" | grep -v "grep" > /dev/null 2>&1
if [ "$?" -eq 1 ]
then
	nohup ./kibana-6.7.1-linux-x86_64/bin/kibana >Kibanalog.log 2>&1 &
	echo "[KB][${time}] Kibana has restarted..."
fi
	sleep 1

done

