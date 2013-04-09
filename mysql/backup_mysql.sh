usage()
{
    echo "$command"
    echo "usage: $command mysql.cnf databasename"
    echo "load mysql database from file"
}

if [ $# != 2 ]
then
    usage
    exit
fi

mysqldump --defaults-extra-file=${1} ${2} > ${2}_$(date +"%Y-%m-%d").mysql
