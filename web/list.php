<?php
	$root = dirname(__FILE__);
	$cache_dir = realpath("../cache");

	$iterator = new DirectoryIterator($cache_dir);

	$leading = "http://192.168.1.150/soundcloud2rss/web/";

	foreach($iterator as $file) {
		if($file->isDot()) {
			continue;
		}

		if($file->isDir()) {
			$id = $file->getBasename();
			if($_GET['static']) {
				echo "<a href={$leading}rss.php?user_id=$id>{$leading}rss.php?user_id=$id</a><br/>";
			} else {
				echo "<a href=rss.php?user_id=$id>rss.php?user_id=$id</a><br/>";
			}
		}
	}
?>