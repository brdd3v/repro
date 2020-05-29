CREATE TABLE posting_queue (url integer not null, content integer not null);

CREATE TABLE incoming_queue (url integer not null, content integer not null);

CREATE TABLE sequence_numbers (url integer primary key, major integer not null, minor integer not null);

CREATE TABLE netserver_manifests (url integer not null, manifest integer not null, unique(url, manifest));

CREATE TABLE manifest_certs (hash integer not null unique, id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(name, id, value, keypair, signature));

CREATE TABLE file_certs (hash integer not null unique, id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(name, id, value, keypair, signature));

CREATE TABLE public_keys (hash integer not null unique, id integer primary key, keydata integer not null);

CREATE TABLE private_keys (hash integer not null unique, id integer primary key, keydata integer not null);

CREATE TABLE merkle_nodes (type integer not null, collection integer not null, level integer not null, prefix integer not null, body integer not null, unique(type, collection, level, prefix));

