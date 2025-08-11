DROP TABLE IF EXISTS todos CASCADE;

CREATE TABLE todos(
  id SERIAL,
  title varchar(255) DEFAULT NULL,
  description varchar(200) DEFAULT NULL,
  priority integer DEFAULT NULL,
  complete boolean DEFAULT false,
  owner_id integer DEFAULT null references users(id),
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users(
  id SERIAL,
  email varchar(255) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  hashed_password varchar(255) DEFAULT NULL,
  is_active boolean DEFAULT true,
  role varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);
