#!/bin/bash
echo "DELETE FROM search_experiment;" | python manage.py dbshell
echo "DELETE FROM search_gene;" | python manage.py dbshell
