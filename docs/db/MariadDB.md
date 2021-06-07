# MariaDB

## reset unknown root password

MariaDB-Service

    systemctl stop mariadb.service
    mysqld_safe --skip-grant-tables --skip-networking &
    
MariaDB

    mysql -u root
    mysql> use mysql;
    mysql> select Host,User,Password,plugin,authentication_string from user;
    mysql> update user set password=PASSWORD("mysql") where User='root';
    mysql> update user set plugin='' where User='root';
    mysql> flush privileges;
    mysql> exit

MariaDB-Service

    mysqladmin shutdown -u root -p
    systemctl start mariadb.service

add local user

    mysql -u root -p mysql
    mysql> create database tw;
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'tw'@'localhost' IDENTIFIED BY 'dsadas' WITH GRANT OPTION;
    mysql> GRANT ALL PRIVILEGES ON tw.* TO 'tw'@'localhost' IDENTIFIED BY 'dsadas' WITH GRANT OPTION;
    mysql> flush privileges;
    mysql> exit
    mysql -u tw -p tw
    mysql> show databases;
    mysql> SELECT USER(), CURRENT_USER();
    mysql> exit
    sudo systemctl restart mariadb.service

add user covid19data

    mysql -u root -p mysql
    mysql> create database flask_covid19;
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'flask_covid19'@'localhost' IDENTIFIED BY 'flask_covid19pwd';
    mysql> GRANT ALL PRIVILEGES ON covid19data.* TO 'flask_covid19'@'localhost' IDENTIFIED BY 'flask_covid19pwd';
    mysql> flush privileges;
    mysql> exit
    mysql -u flask_covid19 -p flask_covid19
    mysql> show databases;
    mysql> SELECT USER(), CURRENT_USER();
    mysql> exit
    sudo systemctl restart mariadb.service
    