# Backend for Sagor
# Instruction for development

- Set up database
```
postgres=# CREATE DATABASE "sagor-database";
CREATE DATABASE
postgres=# CREATE USER sagor WITH SUPERUSER PASSWORD 'sagor';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE "sagor-database" TO sagor;
GRANT
postgres=# 
```

- Copy the environment variables template to your .env file
``cp env.template .env``

# BRAINDUMP
I'm thinking on management commands that are run by crons.
- Publisher command
- Subscriber command

The subscriber will sub to all the topics and filter them w/ regex or smt.
The publisher will publish to all the topics (that'll be deduced from a simple loop over the gateways)

