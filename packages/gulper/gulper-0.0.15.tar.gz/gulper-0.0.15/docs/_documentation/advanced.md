---
# Page settings
layout: documentation-single
title: Advanced
description: In this section you'll learn about some advanced setups and contributing to the tool.
keywords: backups, sqlite-backup, mysql-backup, postgresql-backup, s3-backup, clivern
comments: false
order: 4
hero:
    title: Advanced
    text: In this section you'll learn about some advanced setups and contributing to the tool.
---

## Running with Docker

Create local directories

```
$ mkdir -p gulper/storage
$ mkdir -p gulper/tmp
$ mkdir -p gulper/config
```

Create a config file

```zsh
$ touch gulper/config/config.yaml
```

```yaml
# Storage temp dir
temp_dir: /opt/gulper/tmp

# SQlite state file
state_file: /opt/gulper/config/gulper.db

# Logging configs
logging:
  level: error
  # console or file
  handler: console
  # path to log file if handler is a file
  path: ~

# Stored events configs
event:
  retention: 1 month

storage:
  local_01:
    type: local
    path: /opt/gulper/storage

schedule:
    hourly:
      expression: "0 * * * *"

database:
  gulper_db:
    type: sqlite
    path: /opt/gulper/config/gulper.db
    storage:
      - local_01
    schedule: hourly
    retention: 7 days

  pg_db:
    type: postgresql
    host: pg_db
    username: root
    password: D1q9f0C2&PEW
    database: gulper
    port: 5432
    storage:
      - local_01
    schedule: hourly
    retention: 7 days

  ms_appdb:
    type: mysql
    host: ms_db
    username: appuser
    password: m06rs011e9h9ihuboi7s
    port: 3306
    database:
      - appdb
    storage:
      - local_01
    schedule: hourly
    options:
      quote-names: True
      quick: True
      add-drop-table: True
      add-locks: True
      allow-keywords: True
      disable-keys: True
      extended-insert: True
      single-transaction: True
      create-options: True
      comments: True
      no-tablespaces: True
      net_buffer_length: 16384
    retention: 7 days
```

Create a `docker-compose` file

```zsh
$ touch docker-compose.yaml
```

```yaml
version: '3.8'

services:
  glp_backup:
    image: clivern/gulper:0.0.14
    command: gulper --config /opt/gulper/config/config.yaml cron --daemon
    restart: unless-stopped
    depends_on:
      - pg_db
    volumes:
      - ./gulper:/opt/gulper

  pg_db:
    image: postgres:16.8
    environment:
      POSTGRES_DB: gulper
      POSTGRES_USER: root
      POSTGRES_PASSWORD: D1q9f0C2&PEW
    restart: unless-stopped
    volumes:
      - pg_data:/var/lib/postgresql/data

  ms_db:
    image: 'mysql:8.4'
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=appdb
      - MYSQL_USER=appuser
      - MYSQL_PASSWORD=m06rs011e9h9ihuboi7s
      - MYSQL_ALLOW_EMPTY_PASSWORD=no
    restart: unless-stopped
    volumes:
      - ms_data:/var/lib/mysql

volumes:
  pg_data:
    driver: local

  ms_data:
    driver: local
```

Start the services

```zsh
$ docker-compose up -d
```
