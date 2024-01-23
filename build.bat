echo "Creo ambiente virtuale"
python -m venv venv
echo "Ambiente virtuale creato"
echo "Installo dipendenze"
pip install -r requirements.txt
echo "Dipendenze installate correttamente"
echo "Puoi ora avviare il programma con run.bat"
PAUSE