import soundcloud;
import json;
import sqlite3;
import sys;
from urllib.request import urlopen;
import time;
from math import floor;

user_to_add = sys.argv[1] if sys.argv[0] == "add_to_cacher.py" else sys.argv[0];
_ = urlopen(user_to_add);

import settings;

sc_client = soundcloud.Client(**settings.soundcloud_params);
sql_conn = sqlite3.connect(settings.db_filename);
sql_conn.row_factory = sqlite3.Row;

sql_cur = sql_conn.cursor();
sql_cur.execute("CREATE TABLE IF NOT EXISTS following (USER_ID INTEGER, ADDED INTEGER)");

user = sc_client.get("/resolve", url=user_to_add);
if user.kind != "user":
	raise Exception("Not a user.");

sql_cur.execute("SELECT * FROM following WHERE USER_ID=:id", {"id": user.id});
if not sql_cur.fetchone():
	print("user {} not in database, adding".format(user.permalink));
	with sql_conn:
		sql_cur.execute("INSERT INTO following (USER_ID,ADDED) VALUES (?,?)", (user.id, floor(time.time())));
else:
	print("user {} already in database".format(user.permalink));
