CREATE TABLE manifest_certs (hash integer not null unique, id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(name, id, value, keypair, signature));

CREATE TABLE public_keys (hash integer not null unique, id integer primary key, keydata integer not null);

CREATE TABLE private_keys (hash integer not null unique, id integer primary key, keydata integer not null);

CREATE TABLE revision_certs (hash integer not null unique, id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(name, id, value, keypair, signature));

CREATE TABLE revisions (id integer primary key, data integer not null);

CREATE TABLE revision_ancestry (parent integer not null, child integer not null, unique(parent, child));

CREATE TABLE branch_epochs (hash integer not null unique, branch integer not null unique, epoch integer not null);

