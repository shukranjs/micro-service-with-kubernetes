#!/bin/bash
flask db migrate
flask db upgrade
flask run
exec "$@"
