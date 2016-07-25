<?php
	$root = dirname(__FILE__);
	$cache_dir = realpath("../cache");

	$iterator = new DirectoryIterator($cache_dir);

	foreach($iterator as $file) {
		if($file->isDot()) {
			continue;
		}

		if($file->isDir()) {
			$id = $file->getBasename();
			echo "<a href=rss.php?user_id=$id>rss.php?user_id=$id</a><br/>";
		}
	}
?>