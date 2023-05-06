
# TALENT ACQUISITION TAGGING USING NLP (WIP)

## Installation

- Update your pip and python
- Clone the project using `git clone https://github.com/saidaya/resume-tracking.git`
- `cd resume-tracking`
- Install the libraries using `pip install -r requirements.txt` 
- Run `python -m spacy download en_core_web_lg`
- In main directory of the project, Run `python main.py`


## AWS Server setup .

- create EC2 Ubuntu instance and store the .pem file
- Start the instance and connect the ubuntu through SSH

  - Update using `sudo apt-get update` 
  - Install python using `sudo apt-get install python3`
  - Install pip using `sudo apt-get install python3-pip`
  - Install venv using `sudo apt-get install python3-venv`
  - Insatall git using `sudo apt-get install git`
  - Clone the project files in the root directory using `git clone https://github.com/saidaya/resume-tracking.git`
  - `cd resume-tracking`
  - create venv using `python3 -m venv env` 
  - activate env by `source env/bin/activate`
  - Install the libraries using `pip install -r requirements.txt` 
  - Run `python -m spacy download en_core_web_lg`


## To run with Gunicorn server and add gunicorn server as service on AWS to make it active all the time as long as the instance is running.

- go to system folder using `cd /etc/systemd/system/`
- open service file using `sudo nano gunicorn1.service`
- Copy the below code between the lines and paste into the editor and save the file.
---------------------------------
[Unit]
Description=Gunicorn instance two for my Flask App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/resume-tracking/
Environment="PATH=/home/ubuntu/resume-tracking/env/bin"
ExecStart=/home/ubuntu/resume-tracking/env/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 --timeout  main:app
Restart=always

[Install]
WantedBy=multi-user.target
------------------------------
- save the file using `ctrl+O` => `enter` => `ctrl+X`


## Start service
- To load the daemon `sudo systemctl daemon-reload`
- To start gunicorn as service `sudo systemctl start gunicorn1`
- To check the status of gunicorn `sudo systemctl status gunicorn1`

### Happy Coding !!!


