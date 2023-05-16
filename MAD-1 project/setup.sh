echo "This setup will setup a virtual environment and all install all dependencies in it."
if [ -d ".venv" ];
then
    echo ".venv folder already exists. Please install dependencies using pip."
else
    echo "creating .venv and installing libraries and dependencies using pip"
    python -m venv .venv

fi
. .venv/Scripts/Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
deactivate