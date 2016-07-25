import soundcloud;
import json;
import sqlite3;
import os;

import settings;

if not os.path.exists(settings.cache_directory):
	os.makedirs(settings.cache_directory);

sc_client = soundcloud.Client(**settings.soundcloud_params);
sql_conn = sqlite3.connect(settings.db_filename);
sql_conn.row_factory = sqlite3.Row;

sql_cur = sql_conn.cursor();
sql_cur.execute("CREATE TABLE IF NOT EXISTS following (USER_ID INTEGER, ADDED INTEGER)");

for row in sql_cur.execute("SELECT USER_ID FROM following"):
	api_query = '/users/{}/tracks'.format(row['USER_ID']);

	num = 0;
	tracks = sc_client.get(api_query, limit=15);
	for track in tracks:
		user = track.user;

		file_location = "{}/{}/{}.json".format(settings.cache_directory, user['id'], track.id);
		dir_location = "{}/{}".format(settings.cache_directory, user['id']);

		if num == 0:
			print("checking {}...".format(user['permalink']));

		num += 1;

		if os.path.exists(file_location):
			continue;

		info = {
			"id": track.id,
			"title": track.title,
			"duration": track.duration,
			"timestamp": track.created_at,
			"description": track.description,
			"permalink": track.permalink_url,
			"user": {
				"id": user['id'],
				"name": user['username'],
				"permalink": user['permalink_url'],
				"username": user['permalink']
			}
		};

		if not os.path.exists(dir_location):
			os.makedirs(dir_location);

		with open(file_location, "w") as file:
			json.dump(info, file, **settings.json_settings);