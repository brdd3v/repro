create table info (version INTEGER,  last_opened INTEGER,  first_folder INTEGER,  folder_sort INTEGER);
create table folders (folder_id integer primary key,  parent_id INTEGER,  foldername INTEGER,  unread_count INTEGER,  last_update INTEGER,  type INTEGER,  flags INTEGER,  next_sibling INTEGER,  first_child INTEGER);
create table messages (message_id INTEGER,  folder_id INTEGER,  parent_id INTEGER,  read_flag INTEGER,  marked_flag INTEGER,  deleted_flag INTEGER,  title INTEGER,  sender INTEGER,  link INTEGER,  createddate INTEGER,  date INTEGER,  text INTEGER,  revised_flag INTEGER,  enclosuredownloaded_flag INTEGER,  hasenclosure_flag INTEGER,  enclosure INTEGER);
create table smart_folders (folder_id INTEGER,  search_string INTEGER);
create table rss_folders (folder_id INTEGER,  feed_url INTEGER,  username INTEGER,  last_update_string INTEGER,  description INTEGER,  home_page INTEGER,  bloglines_id INTEGER);
create table rss_guids (message_id INTEGER,  folder_id INTEGER);
