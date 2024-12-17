mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_user = $(shell whoami)
all:
	python3 -m venv venv
	source venv\bin\activate
	python3 -m pip install --upgrade pip
	pip install sqlalchemy
	pip install fastapi
	pip install pydantic
	echo Description=App Pereval > /etc/systemd/system/app-pereval.service
	echo After=network.target >> /etc/systemd/system/app-pereval.service
	echo     >> /etc/systemd/system/app-pereval.service
	echo [Service] >> /etc/systemd/system/app-pereval.service
	echo User=$(current_user)    >> /etc/systemd/system/app-pereval.service
	echo WorkingDirectory=$(mkfile_path)    >> /etc/systemd/system/app-pereval.service
	echo Environment="PATH=$(mkfile_path)/venv/bin"    >> /etc/systemd/system/app-pereval.service
	echo ExecStart=$(mkfile_path)/venv/bin/uvicorn main:app --reload --host 0.0.0.0 >> /etc/systemd/system/app-pereval.service
	echo TimeoutSec=30    >> /etc/systemd/system/app-pereval.service
	echo Restart=always    >> /etc/systemd/system/app-pereval.service
	systemctl daemon-reload
	systemctl enable app-pereval
	systemctl start app-pereval