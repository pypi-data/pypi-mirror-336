---
# Page settings
layout: documentation-single
title: Installation
description: In this section you'll find basic information about Gulper and how to install it and use it properly. If you're first time user then you should read this section first.
keywords: backups, sqlite-backup, mysql-backup, postgresql-backup, s3-backup, clivern
comments: false
order: 1
hero:
    title: Installation
    text: In this section you'll find basic information about Gulper and how to install it and use it properly. If you're first time user then you should read this section first.
---

## What is Gulper?

`Gulper` is a powerful and flexible command-line utility designed for backing up and restoring `SQLite`, `MySQL`, and `PostgreSQL` databases. It offers a range of features to streamline database management tasks, including scheduled backups, multiple storage options, and easy restoration. Some of the features are:

- **Multi-Database Support**: Backup and restore `SQLite`, `MySQL`, and `PostgreSQL` databases.
- **Flexible Storage Options**: Store backups locally or in cloud storage (`AWS S3`, `DigitalOcean Spaces`).
- **Scheduled Backups**: Automate backups using cron-like expressions.
- **Point-in-Time Recovery**: Restore databases to a specific point in time.
- **Compression**: Reduce backup size with built-in `compression` options.
- **Retention Policies**: Automatically manage backup `retention` periods.
- **Logging**: Comprehensive `logging` of all backup and restore activities.


## Why Gulper?

`Gulper` offers several advantages over traditional backup methods and full server backups:

- **Efficiency**: Gulper leverages standard backup tools like `mysqldump`, `pgdump`, and `pgsql`, but optimizes their usage to create a more efficient backup process.
- **Reduced Overhead**: Unlike full server backups, `Gulper` focuses specifically on databases, reducing the overall backup size and resource utilization.
- **Cost-Effective**: By targeting only essential database files, `Gulper` minimizes storage requirements and associated costs compared to full server backups.
- **Faster Backups and Restores**: Database-specific backups are typically quicker to create and restore than full server images, minimizing downtime.
- **Versatility**: `Gulper` acts as a "swiss knife tool" for database backups, supporting multiple database types (`SQLite`, `MySQL`, `PostgreSQL`) and offering features like scheduled backups and flexible storage options.
- **Streamlined Management**: Instead of relying on potentially inefficient bash scripts, `Gulper` provides a comprehensive solution for handling backup tasks across different database types.
- **Complementary to Full Backups**: While full server backups are still necessary for complete disaster recovery, `Gulper` offers a specialized tool for more frequent and targeted database backups

By addressing common inefficiencies in backup scripts and focusing on database-specific needs, `Gulper` provides a more tailored and efficient solution for database backup and restoration compared to full server backups or ad-hoc scripts.


## Installation

#### On Ubuntu

To install `gulper` locally, follow these steps:

```zsh
$ apt update
$ apt install -y mysql-client postgresql-client python3-pip
$ pip3 install gulper
```

This process will:

- Update your package lists
- Install the necessary database clients (`MySQL` and `PostgreSQL`) and python3 `pip`
- Use `pip` to install the `gulper` package

You can verify the setup by checking the versions

```zsh
$ mysqldump --version
$ pg_dump --version
$ pg_dumpall --version
$ psql --version
$ gulper --version
```


#### On Debian

To install `gulper` locally, follow these steps:

```zsh
$ apt update
$ apt install -y default-mysql-client postgresql-client python3-pip
$ pip3 install gulper --break-system-packages
```

This process will:

- Update your package lists
- Install the necessary database clients (`MySQL` and `PostgreSQL`) and python3 `pip`
- Use `pip` to install the `gulper` package

You can verify the setup by checking the versions

```zsh
$ mysqldump --version
$ pg_dump --version
$ pg_dumpall --version
$ psql --version
$ gulper --version
```

