@echo off
echo Installing Python dependencies...
pip install -r requirements.txt
echo Creating database...
python -c "from main import Base, engine; Base.metadata.create_all(bind=engine)"
echo Installation complete!
pause