<?php

$db = new SqlConnector();
$texts = $db->query("SELECT * FROM texts");


while ($text = $texts->fetch_assoc()) {
	echo '<option value="'.$text["id"].'">'.$text["name"].'</option>';
}

?>
