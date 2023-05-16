### General Info
***
This is a README file for the Kanban Application Project created by Parv Pratap Singh (Roll no. 21f1002039) which contains the general know-how to operate the project.
## Technologies
***
A list of technologies used within the project:
* Flask
* Jinja2
* Flask-SQLAlchemy
## Installation
***
Just run setup.sh file to set up the virtual environment and install all python libraries required in the said virtual environment. Command to run-
```
.\setup.sh
```
If the setup fails, please run the following commands on the terminal.
```
python -m venv .venv
.venv/Scripts/Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```
Once the setup is done, use the following script in the terminal to activate the virtual environment-
```
.venv/Scripts/Activate.ps1
```
Then use the following script in the terminal to run the code-
```
python main.py
```
Use the following script to deactivate the virtual environment-
```
deactivate
```