FROM mysql:8
COPY scriptBD.sql /docker-entrypoint-initdb.d/
