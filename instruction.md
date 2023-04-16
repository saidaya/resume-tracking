
# TALENT ACQUISITION TAGGING USING NLP (WIP)

## installation

- Update your pip and python
- Clone the project using `git clone https://github.com/saidaya/resume-tracking.git`
- `cd resume-tracking`
- Install the libraries using `pip install -r requirements.txt` 
- Run `python -m spacy download en_core_web_lg`
- In main directory of the project, Run `python main.py`


##sever setup

create EC2 Linux instance and store the .pem file



## install python

sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python3-venv

# go to root directory
mkdir ResumeRankerAPI/
cd ResumeRankerAPI/


python3 -m venv env
source env/bin/activate


## transfer the code into root folder using filezilla

## install application software requirements
pip install -r requirements.txt

python -m spacy download en_core_web_lg

## gunicorn set up
pip install gunicorn

## add gunicorn server as service that runs the flask app

cd /etc/systemd/system/
sudo nano gunicorn1.service

---------------------------------
[Unit]
Description=Gunicorn instance two for my Flask App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ResumeRankerAPI/
Environment="PATH=/home/ubuntu/ResumeRankerAPI/env/bin"
ExecStart=/home/ubuntu/ResumeRankerAPI/env/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 main:app
Restart=always

[Install]
WantedBy=multi-user.target
------------------------------
ctrl+O
enter
ctrl+X


## start service
sudo systemctl daemon-reload
sudo systemctl start gunicorn1
sudo systemctl enable gunicorn1
sudo systemctl status gunicorn1


