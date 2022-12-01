.PHONY: venv
venv:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf venv
