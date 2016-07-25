<?php
	header("Content-type: application/rss+xml");

	$root = dirname(__FILE__);
	$cache_dir = realpath("../cache");

	function invalid() {
		http_response_code(403);
		die();
	}

	if(!isset($_GET['user_id'])) {
		invalid();
	}

	if(!ctype_digit($_GET['user_id'])) {
		invalid();
	}

	if(file_exists("$cache_dir/{$_GET['user_id']}")) {
		$wanted_dir = "$cache_dir/{$_GET['user_id']}";
		$iterator = new DirectoryIterator($wanted_dir);

		$files = [];

		foreach($iterator as $file) {
			if($file->isDot()) {
				continue;
			}

			$key = $file->getMTime() . "-" . $file->getBasename();

			$data = json_decode(file_get_contents($file->getPathname()), true);

			$files[$key] = $data;
		}
	} else {
		invalid();
	}

	function array_to_xml( $data, &$xml_data ) {
		foreach( $data as $key => $value ) {
			if( is_array($value) ) {
				if( is_numeric($key) ){
					$key = 'item'.$key; //dealing with <0/>..<n/> issues
				}
				$subnode = $xml_data->addChild($key);
				array_to_xml($value, $subnode);
			} else {
				$xml_data->addChild("$key",htmlspecialchars("$value"));
			}
		 }
	}

	krsort($files);
	$files = array_slice($files, 0, 15);

	reset($files);

	$most_recent_data = $files[key($files)];
?>
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">

<channel>
	<title><?php echo $most_recent_data['user']['name']; ?></title>
	<link><?php echo $most_recent_data['user']['permalink']; ?></link>
	<description>Recent uploads for user <?php echo $most_recent_data['user']['username']; ?> on SoundCloud</description>
<?php
	foreach($files as $data) {
		$xmldata = [
			"title" => $data['title'],
			"link" => $data['permalink'],
			"description" => str_replace("\n", "<br/>", $data['description']),
			"pubDate" => date(DATE_RSS, strtotime($data['timestamp'])), 
		];

		$xml = new SimpleXMLElement('<item/>');

		array_to_xml($xmldata, $xml);

		echo str_replace('<?xml version="1.0"?>', '', $xml->asXML());
	}
?>
</channel>

</rss>