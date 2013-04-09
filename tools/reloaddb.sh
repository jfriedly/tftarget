#!/bin/bash
#TODO(jfriedly): Make this script work from any directory
echo "Please enter the MySQL root user's pw at each prompt"
mysql -u root -p tftarget < tools/drop_tables.sql
python manage.py migrate search
mysql -u root -p tftarget < sqldumps/search_experiment.sql
mysql -u root -p tftarget < sqldumps/search_gene.sql
