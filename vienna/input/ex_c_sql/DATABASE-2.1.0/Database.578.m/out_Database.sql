create table info (version, last_opened, first_folder, folder_sort);
create table folders (folder_id integer primary key, parent_id, foldername, unread_count, last_update, type, flags, next_sibling, first_child);
create table messages (message_id, folder_id, parent_id, read_flag, marked_flag, deleted_flag, title, sender, link, createddate, date, text);
create table smart_folders (folder_id, search_string);
create table rss_folders (folder_id, feed_url, username, last_update_string, description, home_page, bloglines_id);
