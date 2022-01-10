create user versionize with password 'versionize';
    alter role versionize set client_encoding to 'utf8';
    alter role versionize set default_transaction_isolation to 'read committed';
    alter role versionize set timezone to 'UTC';
    
   
create database versionize owner versionize;

