CREATE TABLE book
(
	id		 VARCHAR(32) NOT NULL PRIMARY KEY,
	myoid		 INTEGER NOT NULL,
	title		 TEXT NOT NULL,
	edition		 VARCHAR(8) NOT NULL,
	author		 TEXT NOT NULL,
	pdate		 VARCHAR(32) NOT NULL,
	publisher	 TEXT NOT NULL,
	category	 VARCHAR(64) NOT NULL,
	price		 NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
	description	 TEXT NOT NULL,
	language	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	monetary_units	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	quantity	 INTEGER NOT NULL DEFAULT 1,
	binding_type	 VARCHAR(32) NOT NULL,
	location	 TEXT NOT NULL,
	isbn13		 VARCHAR(16) NOT NULL,
	lccontrolnumber	 VARCHAR(64),
	callnumber	 VARCHAR(64),
	deweynumber	 VARCHAR(64),
	front_cover	 BYTEA,
	back_cover	 BYTEA,
	front_cover_fmt	 VARCHAR(8),
	back_cover_fmt	 VARCHAR(8),
	type		 VARCHAR(16) NOT NULL DEFAULT 'Book',
	offsystem_url	 TEXT
	
);

CREATE TABLE book_copy_info
(
	item_oid	 INTEGER NOT NULL,
	myoid		 INTEGER NOT NULL,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY(item_oid, copyid)
);

CREATE TRIGGER book_copy_info_trigger BEFORE DELETE ON book
FOR EACH row 
BEGIN
   DELETE FROM book_copy_info WHERE item_oid = old.myoid;
END;

CREATE TABLE cd
(
	id		 VARCHAR(32) NOT NULL PRIMARY KEY,
	myoid		 INTEGER NOT NULL,
	title		 TEXT NOT NULL,
	artist		 TEXT NOT NULL,
	recording_label	 TEXT NOT NULL,
	rdate		 VARCHAR(32) NOT NULL,
	category	 VARCHAR(64) NOT NULL,
	price		 NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
	description	 TEXT NOT NULL,
	language	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	monetary_units	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	quantity	 INTEGER NOT NULL DEFAULT 1,
	location	 TEXT NOT NULL,
	cdruntime	 VARCHAR(32) NOT NULL,
	cdformat	 VARCHAR(128) NOT NULL,
	cddiskcount	 INTEGER NOT NULL DEFAULT 1,
	cdaudio		 VARCHAR(32) NOT NULL DEFAULT 'Mono',
	cdrecording	 VARCHAR(32) NOT NULL DEFAULT 'Live',
	front_cover	 BYTEA,
	back_cover	 BYTEA,
	front_cover_fmt	 VARCHAR(8),
	back_cover_fmt	 VARCHAR(8),
	type		 VARCHAR(16) NOT NULL DEFAULT 'CD',
	offsystem_url    TEXT
);

CREATE TABLE cd_songs
(
	item_oid	 INTEGER NOT NULL,
	albumnum	 INTEGER NOT NULL DEFAULT 1,
	songnum		 INTEGER NOT NULL DEFAULT 1,
	songtitle	 VARCHAR(256) NOT NULL,
	runtime		 VARCHAR(32) NOT NULL,
	PRIMARY KEY(item_oid, albumnum, songnum)
);

CREATE TABLE cd_copy_info
(
	item_oid	 INTEGER NOT NULL,
	myoid		 INTEGER NOT NULL,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY(item_oid, copyid)
);

CREATE TRIGGER cd_copy_info_trigger BEFORE DELETE ON cd
FOR EACH row 
BEGIN
   DELETE FROM cd_copy_info WHERE item_oid = old.myoid;
   DELETE FROM cd_songs WHERE item_oid = old.myoid;
END;

CREATE TABLE dvd
(
	id		 VARCHAR(32) NOT NULL PRIMARY KEY,
	myoid		 INTEGER NOT NULL,
	title		 TEXT NOT NULL,
	studio		 TEXT NOT NULL,
	rdate		 VARCHAR(32) NOT NULL,
	category	 VARCHAR(64) NOT NULL,
	price		 NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
	description	 TEXT NOT NULL,
	language	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	monetary_units	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	quantity	 INTEGER NOT NULL DEFAULT 1,
	location	 TEXT NOT NULL,
	dvdactor	 TEXT NOT NULL,
	dvdformat	 TEXT NOT NULL,
	dvdruntime	 VARCHAR(32) NOT NULL,
	dvdrating	 VARCHAR(64) NOT NULL,
	dvdregion	 VARCHAR(64) NOT NULL,
	dvddiskcount	 INTEGER NOT NULL DEFAULT 1,
	dvddirector	 TEXT NOT NULL,
	dvdaspectratio	 VARCHAR(64) NOT NULL,
	front_cover	 BYTEA,
	back_cover	 BYTEA,
	front_cover_fmt	 VARCHAR(8),
	back_cover_fmt	 VARCHAR(8),
	type		 VARCHAR(16) NOT NULL DEFAULT 'DVD',
	offsystem_url	 TEXT
);

CREATE TABLE dvd_copy_info
(
	item_oid	 INTEGER NOT NULL,
	myoid		 INTEGER NOT NULL,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY(item_oid, copyid)
);

CREATE TRIGGER dvd_copy_info_trigger BEFORE DELETE ON dvd
FOR EACH row 
BEGIN
   DELETE FROM dvd_copy_info WHERE item_oid = old.myoid;
END;

CREATE TABLE magazine
(
	id		 VARCHAR(32) NOT NULL,
	myoid		 INTEGER NOT NULL,
	title		 TEXT NOT NULL,
	pdate		 VARCHAR(32) NOT NULL,
	publisher	 TEXT NOT NULL,
	category	 VARCHAR(64) NOT NULL,
	price		 NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
	description	 TEXT NOT NULL,
	language	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	monetary_units	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	quantity	 INTEGER NOT NULL DEFAULT 1,
	location	 TEXT NOT NULL,
	mag_volume	 INTEGER NOT NULL DEFAULT 0,
	mag_no		 INTEGER NOT NULL DEFAULT 0,
	lccontrolnumber	 VARCHAR(64),
	callnumber	 VARCHAR(64),
	deweynumber	 VARCHAR(64),
	front_cover	 BYTEA,
	back_cover	 BYTEA,
	front_cover_fmt	 VARCHAR(8),
	back_cover_fmt	 VARCHAR(8),
	type		 VARCHAR(16) NOT NULL DEFAULT 'Journal',
	offsystem_url	 TEXT,
	PRIMARY KEY(id, mag_volume, mag_no)
);

CREATE TABLE magazine_copy_info
(
	item_oid	 INTEGER NOT NULL,
	myoid		 INTEGER NOT NULL,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY(item_oid, copyid)
);

CREATE TRIGGER magazine_copy_info_trigger BEFORE DELETE ON magazine
FOR EACH row 
BEGIN
   DELETE FROM magazine_copy_info WHERE item_oid = old.myoid;
END;

CREATE TABLE videogame
(
	id		 VARCHAR(32) NOT NULL PRIMARY KEY,
	myoid		 INTEGER NOT NULL,
	title		 TEXT NOT NULL,
	developer	 TEXT NOT NULL,
	genre		 VARCHAR(64) NOT NULL,
	rdate		 VARCHAR(32) NOT NULL,
	publisher	 TEXT NOT NULL,
	price		 NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
	description	 TEXT NOT NULL,
	language	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	monetary_units	 VARCHAR(64) NOT NULL DEFAULT 'UNKNOWN',
	quantity	 INTEGER NOT NULL DEFAULT 1,
	location	 TEXT NOT NULL,
	vgrating	 VARCHAR(64) NOT NULL,
	vgplatform	 VARCHAR(64) NOT NULL,
	vgmode		 VARCHAR(16) NOT NULL DEFAULT 'Multiplayer',
	front_cover	 BYTEA,
	back_cover	 BYTEA,
	front_cover_fmt	 VARCHAR(8),
	back_cover_fmt	 VARCHAR(8),
	type		 VARCHAR(16) NOT NULL DEFAULT 'Video Game',
	offsystem_url	 TEXT
);

CREATE TABLE videogame_copy_info
(
	item_oid	 INTEGER NOT NULL,
	myoid		 INTEGER NOT NULL,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY(item_oid, copyid)
);

CREATE TRIGGER videogame_copy_info_trigger BEFORE DELETE ON videogame
FOR EACH row 
BEGIN
   DELETE FROM videogame_copy_info WHERE item_oid = old.myoid;
END;

CREATE TABLE book_borrower
(
	item_oid	 INTEGER NOT NULL,
	memberid	 VARCHAR(16) NOT NULL,
	reserved_date	 VARCHAR(32) NOT NULL,
	duedate		 VARCHAR(32) NOT NULL,
	myoid		 INTEGER PRIMARY KEY AUTOINCREMENT,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	reserved_by	 VARCHAR(128) NOT NULL
);

CREATE TABLE cd_borrower
(
	item_oid	 INTEGER NOT NULL,
	memberid	 VARCHAR(16) NOT NULL,
	reserved_date	 VARCHAR(32) NOT NULL,
	duedate		 VARCHAR(32) NOT NULL,
	myoid		 INTEGER PRIMARY KEY AUTOINCREMENT,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	reserved_by	 VARCHAR(128) NOT NULL
);

CREATE TABLE dvd_borrower
(
	item_oid	 INTEGER NOT NULL,
	memberid	 VARCHAR(16) NOT NULL,
	reserved_date	 VARCHAR(32) NOT NULL,
	duedate		 VARCHAR(32) NOT NULL,
	myoid		 INTEGER PRIMARY KEY AUTOINCREMENT,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	reserved_by	 VARCHAR(128) NOT NULL
);

CREATE TABLE magazine_borrower
(
	item_oid	 INTEGER NOT NULL,
	memberid	 VARCHAR(16) NOT NULL,
	reserved_date	 VARCHAR(32) NOT NULL,
	duedate		 VARCHAR(32) NOT NULL,
	myoid		 INTEGER PRIMARY KEY AUTOINCREMENT,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	reserved_by	 VARCHAR(128) NOT NULL
);

CREATE TABLE videogame_borrower
(
	item_oid	 INTEGER NOT NULL,
	memberid	 VARCHAR(16) NOT NULL,
	reserved_date	 VARCHAR(32) NOT NULL,
	duedate		 VARCHAR(32) NOT NULL,
	myoid		 INTEGER PRIMARY KEY AUTOINCREMENT,
	copyid		 VARCHAR(64) NOT NULL,
	copy_number	 INTEGER NOT NULL DEFAULT 1,
	reserved_by	 VARCHAR(128) NOT NULL
);

CREATE TABLE member
(
	memberid	 VARCHAR(16) NOT NULL PRIMARY KEY DEFAULT 1,
	membersince	 VARCHAR(32) NOT NULL,
	dob		 VARCHAR(32) NOT NULL,
	sex		 VARCHAR(8) NOT NULL DEFAULT 'Female',
	first_name	 VARCHAR(128) NOT NULL,
	middle_init	 VARCHAR(1),
	last_name	 VARCHAR(128) NOT NULL,
	telephone_num	 VARCHAR(32),
	street		 VARCHAR(256) NOT NULL,
	city		 VARCHAR(256) NOT NULL,
	state_abbr	 VARCHAR(2) NOT NULL DEFAULT 'AK',
	zip		 VARCHAR(16) NOT NULL
);

CREATE TABLE member_history
(
	memberid	 VARCHAR(16) NOT NULL,
	item_oid	 INTEGER NOT NULL,
	copyid		 VARCHAR(64) NOT NULL,
	reserved_date	 VARCHAR(32) NOT NULL,
	duedate		 VARCHAR(32) NOT NULL,
	returned_date	 VARCHAR(32) NOT NULL,
	myoid		 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	reserved_by	 VARCHAR(128) NOT NULL,
	type		 VARCHAR(16) NOT NULL,
	item_id		 VARCHAR(32) NOT NULL
);

CREATE TRIGGER member_history_trigger BEFORE DELETE ON member
FOR EACH row 
BEGIN
   DELETE FROM member_history WHERE memberid = old.memberid;
END;

CREATE VIEW cd_borrower_vw AS
SELECT	 item_oid,
	 copy_number,
	 reserved_date,
	 duedate
FROM	 cd_borrower;

CREATE VIEW dvd_borrower_vw AS
SELECT	 item_oid,
	 copy_number,
	 reserved_date,
	 duedate
FROM	 dvd_borrower;


CREATE VIEW book_borrower_vw AS
SELECT	 item_oid,
	 copy_number,
	 reserved_date,
	 duedate
FROM	 book_borrower;

CREATE VIEW magazine_borrower_vw AS
SELECT	 item_oid,
	 copy_number,
	 reserved_date,
	 duedate
FROM	 magazine_borrower;

CREATE VIEW videogame_borrower_vw AS
SELECT	 item_oid,
	 copy_number,
	 reserved_date,
	 duedate
FROM	 videogame_borrower;
