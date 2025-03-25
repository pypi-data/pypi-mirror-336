# Use Ubuntu as the base image
FROM ubuntu:24.04

# Update the package index
RUN apt update

# Install MySQL and PostgreSQL client tools
RUN apt install -y mysql-client postgresql-client python3-pip

# Install gulper & pew
RUN pip3 install gulper==0.0.15 --break-system-packages
RUN pip3 install pew --break-system-packages

# Verify the installation of mysqldump and pg_dump and gulper
RUN mysqldump --version
RUN pg_dump --version
RUN pg_dumpall --version
RUN psql --version
RUN gulper --version

CMD ["gulper"]
