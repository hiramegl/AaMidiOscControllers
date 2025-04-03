# creating a python virtual environment in Raspbian
mkdir /home/<user_name>/projects/oscmidi
python -m venv /home/<user_name>/projects/oscmidi/
cd /home/<user_name>/projects/oscmidi

# installing packages in the virtual environment
./bin/pip install mido
./bin/pip install python-osc

