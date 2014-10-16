#!/bin/sh

DATADIR=/tmp/mysql_tmp
USER=$(whoami)

[ -d ${DATADIR} ] && rm -vrf ${DATADIR}

cat > ./mysql_tmp.cnf <<EOF
[mysqld]
user=${USER}
datadir=${DATADIR}
socket=${DATADIR}.socket
slow_query_log_file=${DATADIR}_slow.log
pid-file=${DATADIR}.pid
skip_networking
log_error=${DATADIR}.err

[mysql_install_db]
ldata=${DATADIR}
user=${USER}

[mysqladmin]
user=root
socket=${DATADIR}.socket

EOF

cat > ./glpi/config/config_db.php <<EOF
<?php
 class DB extends DBmysql {

 var \$dbhost = ':${DATADIR}.socket';
 var \$dbuser 	= 'root';
 var \$dbpassword= '';
 var \$dbdefault	= 'glpi_test';

 }
?>
EOF

trap "rm -rvf ${DATADIR} ${DATADIR}.socket" 2 3

mysql_install_db --defaults-file=./mysql_tmp.cnf
mysqld --defaults-file=./mysql_tmp.cnf
