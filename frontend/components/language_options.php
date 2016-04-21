<?php

	$file_path = __DIR__."/../../src/languages.json";
	$file = file_get_contents($file_path, "r");

	if (!$file) {
		$this->errors->log("b_file_not_found", $file_path);
	}

	$langs = json_decode($file, true);
	foreach ($langs as $k => $l) {
		$language = $langs[$k];
		$selected = "";
		if ($k === "eng") $selected = "";
		echo "<option value='".$k." '".$selected.">".$language."</option>";
	}

?>
