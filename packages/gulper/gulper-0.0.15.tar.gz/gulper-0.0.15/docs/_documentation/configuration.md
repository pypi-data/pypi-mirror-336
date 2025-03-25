---
# Page settings
layout: documentation-single
title: Configuration
description: In this section you will learn how to configure gulper with storages, schedules and databases
keywords: backups, sqlite-backup, mysql-backup, postgresql-backup, s3-backup, clivern
comments: false
order: 2
hero:
    title: Configuration
    text: In this section you will learn how to configure gulper with storages, schedules and databases
---


## Configuration

In this section, you will learn how to configure gulper with storages, schedules, and databases. The configuration is typically done in a YAML file, which we'll explain section by section. You can check [an example here](https://github.com/Clivern/Gulper/blob/main/config.example.yaml)

### General

The general configuration includes settings for temporary directories and state files:

```yaml
# Storage temp dir
temp_dir: /tmp

# SQlite state file
state_file: /etc/gulper.db
```

- `temp_dir`: Specifies the directory for temporary files during backup operations.
- `state_file`: Defines the path to the `SQLite` database file used to store `gulper's` state information.


### Logging

Logging configuration controls how gulper handles log output:

```yaml
logging:
  level: error
  handler: console
  path: ~
```

- `level`: Sets the logging level (e.g., `error`, `info`, `debug`).
- `handler`: Specifies where logs are output (`console` or `file`).
- `path`: If the handler is set to file, this defines the path to the log file.


### Event

Event configuration manages stored events:

```yaml
event:
  retention: 1 month
```

- `retention`: Defines how long `event` data is kept before being purged.


### Storage

Storage configuration defines different storage backends for backups:

```yaml
storage:
  local_01:
    type: local
    path: /opt/backups/

  aws_s3_01:
    type: s3
    access_key_id: your_access_key_id
    secret_access_key: your_secret_access_key
    bucket_name: your_bucket_name
    region: your_region
    path: /

  do_s3_01:
    type: s3
    access_key_id: your_access_key_id
    secret_access_key: your_secret_access_key
    endpoint_url: https://nyc3.digitaloceanspaces.com
    bucket_name: your_bucket_name
    region: nyc3
    path: /team_name/db_backups
```

This section defines three storage options:

- A `local storage` on the file system
- An `AWS S3` bucket
- A `DigitalOcean Spaces` bucket (which uses `S3-compatible` API)


### Schedule

Schedule configuration defines when backups should run:

```yaml
schedule:
    hourly:
      expression: "0 * * * *"
```

This example sets up an hourly schedule using a cron expression. you can use [cron guru](https://crontab.guru/) to build cron expression


### Database

Database configuration specifies the databases to be backed up and their settings:

```yaml
database:
  db01:
    type: mysql
    host: localhost
    username: root
    password: your_password
    port: 3306
    database:
      - db01
      - db02
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
      skip-ssl: True
      no-tablespaces: True
      net_buffer_length: 16384
    retention: 3 months

  db02:
    type: postgresql
    host: localhost
    username: root
    password: your_password
    database: db01
    port: 5432
    storage:
      - aws_s3_01
    schedule: hourly
    retention: 7 days

  db03:
    type: sqlite
    path: /opt/app/opswork.db
    storage:
      - local_02
    schedule: hourly
    retention: 1 year
```

This section defines three database configurations:

- A `MySQL` database with multiple databases and specific `mysqldump` options
- A `PostgreSQL` database
- A `SQLite` database

Each configuration specifies:

- Database type and connection details
- Which `storage` to use for backups
- Backup `schedule`
- `Retention` period for backups
- Database-specific options (e.g., `mysqldump` options for `MySQL`)

By adjusting these configurations, you can customize `gulper` to handle various `database types`, `storage solutions`, and `backup schedules` according to your specific needs.

