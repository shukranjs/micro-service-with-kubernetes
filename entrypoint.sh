#!/bin/bash
echo "Geeks for Geeks"
flask db migrate
flask db upgrade
flask run
exec "$@"
