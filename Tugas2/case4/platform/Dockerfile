FROM php:8.2-apache

# system tools + mysql client + build deps for intl
RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    supervisor curl socat default-mysql-client \
    libicu-dev pkg-config; \
  \
  # build PHP extensions
  docker-php-ext-install -j"$(nproc)" mysqli pdo_mysql intl; \
  \
  # optional: enable opcache (already present in base image)
  docker-php-ext-enable opcache; \
  \
  # slim down image (keep ICU runtime, drop -dev if you like)
  apt-get purge -y pkg-config; \
  apt-get autoremove -y; \
  rm -rf /var/lib/apt/lists/*

COPY start.sh /tmp/
COPY supervisord.conf /tmp/supervisord.conf
EXPOSE 80
ENV SESSIONAGE=60 REAUTHENTICATION=60 IPEXPIRE=120
ENTRYPOINT ["sh","-c","/tmp/start.sh"]
