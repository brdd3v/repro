 
-- schema for the sql database. this file is objcopied into
-- a string constant, as the symbol:
-- 
-- extern char const _binary_schema_null_start[];
--
-- and emitted as schema.o at compile time. it is used by
-- database.cc when initializing a fresh sqlite db.


-- copyright (C) 2002 graydon hoare <graydon@pobox.com>
-- all rights reserved.
-- licensed to the public under the terms of the GNU GPL 2.1+
-- see the file COPYING for details


-- primary data structures concerned with storing and 
-- versionning state-of-tree configurations

CREATE TABLE schema_version
	(
	version primary key
	);

CREATE TABLE files
	(
	id primary key,   -- strong hash of file contents
	data not null     -- compressed, encoded contents of a file
	); 

CREATE TABLE file_deltas
	(	
	id not null,      -- strong hash of file contents
	base not null,    -- joins with files.id or file_deltas.id
	delta not null,   -- rdiff to construct current from base
	unique(id, base)
	);

CREATE TABLE manifests
	(
	id primary key,      -- strong hash of all the entries in a manifest
	data not null        -- compressed, encoded contents of a manifest
	);

CREATE TABLE manifest_deltas
	(
	id not null,         -- strong hash of all the entries in a manifest
	base not null,       -- joins with either manifest.id or manifest_deltas.id
	delta not null,      -- rdiff to construct current from base
	unique(id, base)
	);

-- structures for managing RSA keys and file / manifest certs
 
CREATE TABLE public_keys
	(
	id primary key,     -- key identifier chosen by user
	keydata not null    -- RSA public params
	);

CREATE TABLE private_keys
	(
	id primary key,     -- as in public_keys (same identifiers, in fact)
	keydata not null    -- encrypted RSA private params
	);

CREATE TABLE manifest_certs
	(
	id not null,        -- joins with manifests.id or manifest_deltas.id
	name not null,      -- opaque string chosen by user
	value not null,     -- opaque blob
	keypair not null,   -- joins with public_keys.id
	signature not null, -- RSA/SHA1 signature of [manifest,name,val]
	unique(id, name, value, keypair, signature)
	);

CREATE TABLE file_certs
	(
	id not null,        -- joins with files.id or file_deltas.id
	name not null,      -- opaque string chosen by user
	value not null,     -- opaque blob
	keypair not null,   -- joins with public_keys.id
	signature not null, -- RSA/SHA1 signature of [manifest,name,val]
	unique(id, name, value, keypair, signature)
	);

-- structures for managing our relationship to netnews

CREATE TABLE posting_queue
	(
	server not null,    -- DNS name of a news server to post to
	newsgroup not null, -- name of a news group to post to
	old_id not null,    -- joins with manifests.id or manifest_deltas.id
	new_id not null,    -- joins with manifests.id or manifest_deltas.id
	unique(server, old_id, new_id)
	);

CREATE TABLE sequence_numbers
	(
	server not null,    -- DNS name of a news server to read from
	newsgroup not null, -- name of a news group to read from
	seq not null,       -- last article sequence number we got
	unique(server, newsgroup)
	);
