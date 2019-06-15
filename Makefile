
venv:
	@rm -rf venv
	@virtualenv --no-download -p python2.7 venv
	venv/bin/pip install -r REQUIREMENTS
	@touch $@


static_generate:
	rm -rf static/.webassets-cache
	venv/bin/python manage.py assets build


run_static_server:
	venv/bin/python -m SimpleHTTPServer 8001
