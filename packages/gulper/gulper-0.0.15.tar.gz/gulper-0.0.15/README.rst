.. image:: https://images.unsplash.com/photo-1589995186011-a7b485edc4bf
  :width: 700
  :alt: Cover Photo

.. image:: https://img.shields.io/pypi/v/gulper.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/gulper/
.. image:: https://img.shields.io/badge/Docker-0.0.15-1abc9c.svg
    :alt: Docker Image
    :target: https://hub.docker.com/r/clivern/gulper/tags
.. image:: https://github.com/Clivern/Gulper/actions/workflows/ci.yml/badge.svg?branch=main
    :alt: Build Status
    :target: https://github.com/Clivern/Gulper/actions/workflows/ci.yml
.. image:: https://static.pepy.tech/badge/gulper
    :alt: Downloads
    :target: https://pepy.tech/projects/gulper

|

=======
Gulper
=======

``Gulper`` is a powerful and flexible command-line utility designed for backing up and restoring ``SQLite``, ``MySQL``, and ``PostgreSQL`` databases. It offers a range of features to streamline database management tasks, including scheduled backups, multiple storage options, and easy restoration.


Features
========

- **Multi-Database Support**: Backup and restore ``SQLite``, ``MySQL``, and ``PostgreSQL`` databases.
- **Flexible Storage Options**: Store backups locally or in cloud storage (``AWS S3``, ``DigitalOcean Spaces``).
- **Scheduled Backups**: Automate backups using cron-like expressions.
- **Point-in-Time Recovery**: Restore databases to a specific point in time.
- **Compression**: Reduce backup size with built-in ``compression`` options.
- **Retention Policies**: Automatically manage backup ``retention`` periods.
- **Logging**: Comprehensive ``logging`` of all backup and restore activities.


Installation
============

To install ``gulper``, use the following command

.. code-block::

  $ pip install gulper


Configuration
=============

Gulper uses a YAML configuration file to manage settings. By default, it looks for the configuration at ``/etc/config.yaml``. You can specify a different path using the ``--config`` option.

Example configuration:

.. code-block:: yaml

  temp_dir: /tmp
  state_file: /etc/gulper.db

  logging:
    level: error
    handler: console
    path: ~

  event:
    retention: 1 month

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

  schedule:
    hourly:
      expression: 0 * * * *

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
      storage:
        - aws_s3_01
      schedule: hourly
      retention: 7 days

    db03:
      type: sqlite
      path: /opt/app/opswork.db
      storage:
        - aws_s3_01
      schedule: hourly
      retention: 1 year


Usage
======

Backup Commands

- List backups: ``gulper [--config PATH] backup list [--db DB] [--since SINCE] [--json]``
- Run backup: ``gulper [--config PATH] backup run DB [--json]``
- Get backup details: ``gulper [--config PATH] backup get BACKUP_ID [--json]``
- Delete backup: ``gulper [--config PATH] backup delete BACKUP_ID [--json]``

Restore Commands

- Restore from backup: ``gulper [--config PATH] restore run BACKUP_ID [--json]``
- Restore specific database: ``gulper [--config PATH] restore db DB [--json]``

Cron Command

- Run scheduled backups: ``gulper [--config PATH] cron [--daemon]``

Event Command

- List events: ``gulper [--config PATH] event list [--db DB] [--since SINCE] [--json]``


Examples
=========

1. Backup a database (``MySQL`` or ``SQLite`` or ``PostgreSQL``):

.. code-block::

   $ gulper --config config.yaml backup run $dbName


2. Restore a database from a specific backup or the latest db backup

.. code-block::

   $ gulper --config config.yaml restore run $backupId
   $ gulper --config config.yaml restore db $dbName


3. List all backups or for a specific database:

.. code-block::

   $ gulper --config config.yaml backup list
   $ gulper --config config.yaml backup list --json
   $ gulper --config config.yaml backup list --db $dbName
   $ gulper --config config.yaml backup list --db $dbName --since "3 hours ago"


4. Run scheduled backups in ``daemon`` mode:

.. code-block::

  $ gulper --config config.yaml cron --daemon


5. To get a list of ``events``.

.. code-block::

  $ gulper --config config.yaml event list
  $ gulper --config config.yaml event list --db $dbName --since "1 hour ago"
  $ gulper --config config.yaml event list --json


Versioning
==========

For transparency into our release cycle and in striving to maintain backward
compatibility, Tyran is maintained under the `Semantic Versioning guidelines`_
and release process is predictable and business-friendly.

.. _Semantic Versioning guidelines: https://semver.org/

See the `Releases section of our GitHub project`_ for changelogs for each release
version of Tyran. It contains summaries of the most noteworthy changes made
in each release. Also see the `Milestones section`_ for the future roadmap.

.. _Releases section of our GitHub project: https://github.com/Clivern/Gulper/releases
.. _Milestones section: https://github.com/Clivern/Gulper/milestones


Bug tracker
===========

If you have any suggestions, bug reports, or annoyances please report them to
our issue tracker at https://github.com/Clivern/Gulper/issues


Security Issues
===============

If you discover a security vulnerability within Gulper, please send an email to
`hello@clivern.com <mailto:hello@clivern.com>`_

.. _hello@clivern.com <mailto:hello@clivern.com>: mailto:hello@clivern.com


Contributing
============

We are an open source, community-driven project so please feel free to join
us. see the `contributing guidelines`_ for more details.

.. _contributing guidelines: CONTRIBUTING.rst


License
=======

© 2025, Gulper. Released under `MIT License`_.

.. _MIT License: https://opensource.org/licenses/mit-license.php

**Gulper** is authored and maintained by `Clivern <https://github.com/clivern>`_.

