#!/bin/sh
set -e
exec /usr/bin/supervisord -c /tmp/supervisord.conf
