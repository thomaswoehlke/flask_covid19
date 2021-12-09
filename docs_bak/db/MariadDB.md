# MariaDB

## reset unknown root password

````bash
    systemctl stop mariadb.service
    mysqld_safe --skip-grant-tables --skip-networking &
````

## MariaDB user and Database

````bash
    mysql -u root
````

````mysql
    use mysql;
    select Host,User,Password,plugin,authentication_string from user;
    update user set password=PASSWORD("mysql") where User='root';
    update user set plugin='' where User='root';
    flush privileges;
    exit
````

## MariaDB-Service

````bash
    mysqladmin shutdown -u root -p
    systemctl start mariadb.service
````

## add local user

````bash
    mysql -u root -p mysql
````

````mysql
    create database tw;
    GRANT ALL PRIVILEGES ON *.* TO 'tw'@'localhost' IDENTIFIED BY 'dsadas' WITH GRANT OPTION;
    GRANT ALL PRIVILEGES ON tw.* TO 'tw'@'localhost' IDENTIFIED BY 'dsadas' WITH GRANT OPTION;
    flush privileges;
    exit
````

````bash
    mysql -u tw -p tw
````

````mysql
    show databases;
    SELECT USER(), CURRENT_USER();
    exit
````

````bash
    sudo systemctl restart mariadb.service
````

## add user covid19data

````bash
    mysql -u root -p mysql
````

````mysql
    mysql> create database flask_covid19;
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'flask_covid19'@'localhost' IDENTIFIED BY 'flask_covid19pwd';
    mysql> GRANT ALL PRIVILEGES ON covid19data.* TO 'flask_covid19'@'localhost' IDENTIFIED BY 'flask_covid19pwd';
    mysql> flush privileges;
    mysql> exit
````

````bash
    mysql -u flask_covid19 -p flask_covid19
````

````mysql
    show databases;
    SELECT USER(), CURRENT_USER();
    exit
````

````bash
    sudo systemctl restart mariadb.service
````
