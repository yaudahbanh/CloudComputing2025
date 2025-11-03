#!/usr/bin/env bash
set -euo pipefail

mkdir -p app nginx

cat > app/index.php <<'EOF'
<?php
echo "<h1>Hello from Nginx and PHP-FPM (Alpine)!</h1>";
echo "<p>This is a simple PHP application running in Docker containers.</p>";
echo "<p>Check out <a href=\"info.php\">PHP Info</a>.</p>";
?>
EOF

cat > app/info.php <<'EOF'
<?php phpinfo();
EOF

cat > nginx/nginx.conf <<'EOF'
server {
    listen 80;
    index index.php index.html;
    root /var/www/html;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass application-processor:9000;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
}
EOF

docker network create app-network 2>/dev/null || true
docker stop web-server 2>/dev/null || true
docker rm web-server 2>/dev/null || true
docker stop application-processor 2>/dev/null || true
docker rm application-processor 2>/dev/null || true

docker run -dit --name application-processor \
  --network app-network \
  -v "$(pwd)/app":/var/www/html \
  php:8.2-fpm-alpine

docker run -dit --name web-server \
  --network app-network \
  -p 8000:80 \
  -v "$(pwd)/nginx/nginx.conf":/etc/nginx/conf.d/default.conf:ro \
  -v "$(pwd)/app":/var/www/html:ro \
  nginx:alpine