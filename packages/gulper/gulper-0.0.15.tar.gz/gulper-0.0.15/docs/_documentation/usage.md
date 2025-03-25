---
# Page settings
layout: documentation-single
title: Usage
description: In this section you will learn how to use gulper to backup, restore and list backups.
keywords: backups, sqlite-backup, mysql-backup, postgresql-backup, s3-backup, clivern
comments: false
order: 3
hero:
    title: Usage
    text: In this section you will learn how to use gulper to backup, restore and list backups.
---

## Backup Commands

`Gulper` provides several commands for managing `backups`:

### List backups

To list all backups or backups for a specific database:

```
gulper [--config PATH] backup list [--db DB] [--since SINCE] [--json]
```

Options:
- `--db DB`: Specify a database name to list backups for
- `--since SINCE`: List backups since a specific time (e.g. "3 hours ago")
- `--json`: Output results in JSON format

### Run backup

To run a backup for a specific database:

```
gulper [--config PATH] backup run DB [--json]
```

### Get backup details

To get details about a specific backup:

```
gulper [--config PATH] backup get BACKUP_ID [--json]
```

### Delete backup

To delete a specific backup:

```
gulper [--config PATH] backup delete BACKUP_ID [--json]
```

## Restore Commands

Gulper offers two main restore commands:

### Restore from backup

To restore from a specific backup:

```
gulper [--config PATH] restore run BACKUP_ID [--json]
```

### Restore specific database

To restore the latest `backup` for a specific `database`:

```
gulper [--config PATH] restore db DB [--json]
```

## Cron Command

To run scheduled backups:

```
gulper [--config PATH] cron [--daemon]
```

Use the `--daemon` flag to run in daemon mode.

## Event Command

To list events:

```
gulper [--config PATH] event list [--db DB] [--since SINCE] [--json]
```

Options:
- `--db DB`: List events for a specific `database`
- `--since SINCE`: List events since a specific time (e.g. "1 hour ago")
- `--json`: Output results in `JSON` format

## Examples

- Backup a database (`MySQL`, `SQLite`, or `PostgreSQL`):

```
$ gulper --config config.yaml backup run $dbName
```

- Restore a database from a specific backup or the latest db `backup`:

```
$ gulper --config config.yaml restore run $backupId
$ gulper --config config.yaml restore db $dbName
```

- List all backups or for a specific `database`:

```
$ gulper --config config.yaml backup list
$ gulper --config config.yaml backup list --json
$ gulper --config config.yaml backup list --db $dbName
$ gulper --config config.yaml backup list --db $dbName --since "3 hours ago"
```

- Run scheduled backups in `daemon` mode:

```
$ gulper --config config.yaml cron --daemon
```

- List `events`:

```
$ gulper --config config.yaml event list
$ gulper --config config.yaml event list --db $dbName --since "1 hour ago"
$ gulper --config config.yaml event list --json
```

These commands provide a comprehensive set of tools for managing database `backups`, `restorations`, and monitoring `events` with `Gulper`.

