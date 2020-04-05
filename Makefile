initialise-environment:
	@ echo "Creating a Virtual Environment"
	@ python -m venv $(CURDIR)/env && source env/Scripts/activate && pip install -r requirements.txt