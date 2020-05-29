CREATE TABLE manifest_certs (hash integer not null unique, id integer not null, name integer not null, value integer not null, keypair integer not null, signature integer not null, unique(name, id, value, keypair, signature));

CREATE TABLE revisions (id integer primary key, data integer not null);

CREATE TABLE revision_ancestry (parent integer not null, child integer not null, unique(parent, child));

CREATE TABLE db_vars (domain integer not null, name integer not null, value integer not null, unique(domain, name));

CREATE TABLE next_roster_node_number (node integer primary key);

CREATE TABLE files (id integer primary key, data integer not null);

CREATE TABLE file_deltas (id integer not null, base integer not null, delta integer not null, unique(id, base));

CREATE TABLE rosters (id integer primary key, checksum integer not null,  data integer not null);

CREATE TABLE roster_deltas (id integer primary key, checksum integer not null,  base integer not null, delta integer not null);

CREATE TABLE heights (revision integer not null, height integer not null, unique(revision, height));

CREATE TABLE branch_epochs (hash integer not null unique, branch integer not null unique, epoch integer not null);

CREATE TABLE public_keys (id integer primary key, name integer not null, keydata integer not null);

CREATE TABLE revision_certs (hash integer not null unique, revision_id integer not null, name integer not null, value integer not null, keypair_id integer not null, signature integer not null, unique(name, value, revision_id, keypair_id, signature));

