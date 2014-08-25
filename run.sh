#!/usr/bin/env bash
export PDB_VIS_SETTINGS='../dev_settings.py'
gunicorn --log-file=- -k gevent -b 127.0.0.1:5000 pdb_vis.application:app
