-- init.sql: create database if not exists
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'booking_db') THEN
      CREATE DATABASE booking_db;
   END IF;
END
$$;
