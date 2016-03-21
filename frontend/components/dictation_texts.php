<?php

$db = new SqlConnector();
$texts = $db->query("SELECT texts.name, texts.id
					FROM texts, audio
					WHERE texts.id = audio.text_id;");


while ($text = $texts->fetch_assoc()) {
	echo '<option value="'.$text["id"].'">'.$text["name"].'</option>';
}

?>
