CREATE TABLE files (id integer primary key, data integer not null);

CREATE TABLE file_deltas (id integer not null, base integer not null, delta integer not null, unique(id, base));

CREATE TABLE manifests (id integer primary key, data integer not null);

CREATE TABLE manifest_deltas (id integer not null, base integer not null, delta integer not null, unique(id, base));

CREATE TABLE revisions (id integer primary key, data integer not null);

CREATE TABLE revision_ancestry (parent integer not null, child integer not null, unique(parent, child));

CREATE TABLE public_keys (hash integer not null unique, id integer primary key, keydata integer not null);

CREATE TABLE private_keys (hash integer not null unique, id integer primary key, keydata integer not null);

CREATE TABLE manifest_certs (hash integer not null unique, id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(name, id, value, keypair, signature));

CREATE TABLE revision_certs (hash integer not null unique, id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(name, id, value, keypair, signature));

CREATE TABLE merkle_nodes (type integer not null, collection integer not null, level integer not null, prefix integer not null, body integer not null, unique(type, collection, level, prefix));

