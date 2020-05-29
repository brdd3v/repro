CREATE TABLE schema_version (version integer primary key);

CREATE TABLE files (id integer primary key, data integer not null);

CREATE TABLE file_deltas (id integer not null, base integer not null, delta integer not null, unique(id, base));

CREATE TABLE manifests (id integer primary key, data integer not null);

CREATE TABLE manifest_deltas (id integer not null, base integer not null, delta integer not null, unique(id, base));

CREATE TABLE public_keys (id integer primary key, keydata integer not null);

CREATE TABLE private_keys (id integer primary key, keydata integer not null);

CREATE TABLE manifest_certs (id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(id, name, value, keypair, signature));

CREATE TABLE file_certs (id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(id, name, value, keypair, signature));

CREATE TABLE posting_queue (server integer not null, newsgroup integer not null, old_id integer not null, new_id integer not null, unique(server, old_id, new_id));

CREATE TABLE sequence_numbers (server integer not null, newsgroup integer not null, seq integer not null, unique(server, newsgroup));

