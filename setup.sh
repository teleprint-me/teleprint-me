#!/usr/bin/env bash

function setup_virtualenv() {
    virtualenv venv
    source venv/bin/activate
    pip install -U pip bpython
    deactivate
}

function setup_requirements() {
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
}

setup_virtualenv
setup_requirements

echo
echo Use \'source venv/bin/activate\' to activate the virtualenv.
echo
echo *********
echo * Done! *
echo *********
