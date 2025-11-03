#!/bin/sh
docker stop mysql1 2>/dev/null
docker rm mysql1 2>/dev/null

docker run -dit --name mysql1 \
  -v mysql_data_volume:/var/lib/mysql \
  -e MYSQL_DATABASE=mydb \
  -e MYSQL_ROOT_PASSWORD='mydb6789tyui' \
  -e MYSQL_USER='appuser' \
  -e MYSQL_PASSWORD='mydb6789tyui' \
  mysql:8.0