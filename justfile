set dotenv-load := true

setup:
	python3 -m venv ./venv && source ./venv/bin/activate && pip install pip --upgrade && pip install -r requirements.txt && pip install -e . || rm -r venv

format:
	source ./venv/bin/activate && isort . && black .

check:
  source ./venv/bin/activate && node ./node_modules/.bin/pyright ./notion

jupyterlab:
  source ./venv/bin/activate && jupyter lab
