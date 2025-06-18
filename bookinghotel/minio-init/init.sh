#!/bin/sh
set -e

sleep 10

mc alias set myminio http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mb myminio/media || true
mc anonymous set download myminio/media
