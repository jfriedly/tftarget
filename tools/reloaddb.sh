#!/bin/bash
#TODO(jfriedly): Make this script work from any directory
echo "Please enter the MySQL root user's pw at each prompt"
mysql -uroot -p tftarget < tools/drop_tables.sql
python manage.py migrate search
mysql -uroot -p tftarget < sqldumps/search_experiment_expt_type.sql
mysql -uroot -p tftarget < sqldumps/search_experiment.sql
mysql -uroot -p tftarget < sqldumps/search_experiment_transcription_factor.sql
mysql -uroot -p tftarget < sqldumps/search_experimenttype.sql
mysql -uroot -p tftarget < sqldumps/search_transcriptionfactor.sql
