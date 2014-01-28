#!/bin/sh

#
#    load_mysql.sh - small script to load database backup with mysql config file
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright (C) 2013 Kevin Roy <kiniou@gmail.com>



#set -x
command=$(basename $0)

usage()
{
    echo "$command"
    echo "usage: $command file.sql mysql.cnf databasename"
    echo "load mysql database from file"
}

if [ $# != 3 ]
then
    usage
    exit
fi

#ZENITY_PROGRESS="zenity --width 550 --progress --auto-close --auto-kill --title \"Importing ${1} into MySQL database ${3}\" --text \"Importing into the database\""

mysql --defaults-extra-file=${2} -v -v -v <<EOFMYSQL
DROP DATABASE IF EXISTS \`${3}\`;
CREATE DATABASE \`${3}\`;
EOFMYSQL

(pv -n ${1} | mysql --defaults-extra-file=${2} -D ${3}) 2>&1 | dialog --gauge 'Progress' 7 70
