
# TALENT ACQUISITION TAGGING USING NLP (WIP)

## Installation

- Update your pip and python
- Clone the project using `git clone https://github.com/saidaya/resume-tracking.git`
- `cd resume-tracking`
- Install the libraries using `pip install -r requirements.txt` 
- Run `python -m spacy download en_core_web_lg`
- In main directory of the project, Run `python main.py`


## AWS Server setup & Running the Flask code.

- create EC2 Ubuntu instance and store the .pem file
- Start the instance and connect the ubuntu through SSH
- Install python

  - Update using `sudo apt-get update` 
  - Install python using `sudo apt-get install python3`
  - Install pip using `sudo apt-get install python3-pip`
  - Install venv using `sudo apt-get install python3-venv`
  - Clone the project files in the root directory using `git clone https://github.com/saidaya/resume-tracking.git`
  - `cd resume-tracking`
  - Install the libraries using `pip install -r requirements.txt` 
  - Run `python -m spacy download en_core_web_lg`
  - In main directory of the project, Run `python main.py`


## Gunicorn set up
- Install gunicorn using `pip install gunicorn`

## To add gunicorn server as service

```
cd /etc/systemd/system/
sudo nano gunicorn1.service
---------------------------------
[Unit]
Description=Gunicorn instance two for my Flask App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/resume-tracking/
Environment="PATH=/home/ubuntu/resume-tracking/env/bin"
ExecStart=/home/ubuntu/resume-tracking/env/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 main:app
Restart=always

[Install]
WantedBy=multi-user.target
------------------------------
ctrl+O
enter
ctrl+X
```

## Start service
- To load the daemon `sudo systemctl daemon-reload`
- To start gunicorn as service `sudo systemctl start gunicorn1`
- To Enable gunicorn `sudo systemctl enable gunicorn1`
- To check the status of gunicorn `sudo systemctl status gunicorn1`
### Happy Coding !!!


