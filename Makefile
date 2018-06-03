.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	detox

ci:
	pipenv run py.test -n 8 --boxed --junitxml=report.xml

flake8:
	pipenv run flake8 mailer

coverage:
	pipenv run py.test --cov.config .coveragerc --verbose --cov-report term xml --cov=mailer tests

publish:
	pip install pipenv --upgrade
	pipenv install
