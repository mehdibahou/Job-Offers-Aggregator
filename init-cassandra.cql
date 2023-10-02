-- Create a keyspace for your application
CREATE KEYSPACE IF NOT EXISTS mykeyspace
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

--Use the new keyspace
    USE mykeyspace;

-- Create a table for your application
CREATE TABLE IF NOT EXISTS mytable (
  id UUID PRIMARY KEY,
  name TEXT,
  age INT
);
