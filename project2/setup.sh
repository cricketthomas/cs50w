pip3 install -r requirements.txt
set FLASK_APP=application.py
set FLASK_DEBUG=1
flask run --no-reload

pip3 install -r requirements.txt
export FLASK_APP=application.py
#export FLASK_DEBUG=1
flask run --no-reload