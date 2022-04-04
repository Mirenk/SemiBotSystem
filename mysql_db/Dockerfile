FROM mysql/mysql-server

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

COPY mysqld_charset.cnf /etc/mysql/conf.d/mysqld_charset.cnf
RUN chmod 644 /etc/mysql/conf.d/mysqld_charset.cnf