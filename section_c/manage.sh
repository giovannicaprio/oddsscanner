#!/bin/bash

case "$1" in
  "start")
    docker-compose up --build
    ;;
  "stop")
    docker-compose down
    ;;
  "rebuild")
    docker-compose down
    docker-compose build --no-cache
    docker-compose up
    ;;
  "clean")
    docker-compose down -v
    docker-compose rm -f
    ;;
  "logs")
    docker-compose logs -f
    ;;
  *)
    echo "Usage: $0 {start|stop|rebuild|clean|logs}"
    exit 1
    ;;
esac 