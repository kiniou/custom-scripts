#!/bin/sh

usage()
{
    echo "$0"
    echo "usage: $0 mysql.cnf databasename"
    echo "backup mysql database to file"
}

if [ $# -lt 2 ]
then
    usage
    exit
fi

tablename="full"
[ -z ${3} ] || tablename="${3}"

FILENAME=${2}_$(date +"%Y-%m-%d").${tablename}.mysql

FINAL_FILENAME=${FILENAME}

num=-1
while [ -e ${FINAL_FILENAME} ]
do
    num=$(expr ${num} + 1)
    FINAL_FILENAME="${FILENAME}.${num}"
done

mysqldump --defaults-extra-file=${1}  --extended-insert=FALSE --complete-insert=TRUE ${2} ${3} > ${FINAL_FILENAME}
