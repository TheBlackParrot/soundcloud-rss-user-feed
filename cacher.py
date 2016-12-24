from __future__ import unicode_literals;
import soundcloud;
import json;
import sqlite3;
import os;
import urllib.request;
try: 
	from BeautifulSoup import BeautifulSoup;
except ImportError:
	from bs4 import BeautifulSoup;

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
	if not len(tracks):
		'''
			currently waiting on https://github.com/rg3/youtube-dl/issues/11181

			UPDATE: i give up, i'm scraping artist pages now
		'''

		print("no API response for {}, probably blocked.".format(row['USER_ID']));

		user = sc_client.get('/users/{}'.format(row['USER_ID']));
		tracks_page = '{}/tracks'.format(user.permalink_url);

		dir_location = "{}/{}".format(settings.cache_directory, user.id);

		if not os.path.exists(dir_location):
			os.makedirs(dir_location);

		if num == 0:
			print("scraping {}...".format(user.permalink));

		num += 1;

		with urllib.request.urlopen(tracks_page) as response:
			html = response.read();

			soup = BeautifulSoup(html, "html.parser");

			for article in soup.find_all(class_='audible'):
				track = article.find('a', attrs={"itemprop": "url"}, href=True);
				timestamp = article.find('time');

				file_location = "{}/{}.json".format(dir_location, track['href'].split("/")[-1:][0]);

				if os.path.exists(file_location):
					continue;

				info = {
					"id": -1,
					"title": track.text,
					"duration": -1,
					"timestamp": timestamp.text,
					"description": "API request was rejected, unable to scrape for description.",
					"permalink": "http://soundcloud.com{}".format(track['href']),
					"user": {
						"id": -1,
						"name": user.username,
						"permalink": user.permalink_url,
						"username": user.permalink
					}
				};

				with open(file_location, "w") as file:
					json.dump(info, file, **settings.json_settings);

			print("finished");

	else:
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

		print("finished");