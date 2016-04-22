<?php
	require_once __DIR__."/../inc/SqlConnector.php";
	$db = new SqlConnector();

	$username = $_POST["username"];
	$limit = $_POST["limit"];
	$offset = $_POST["offset"];

	$dictations = $db->getAllDictationsForUser($username, $limit, $offset);
	$out = array();

	while ($dict = $dictations->fetch_assoc()) {
		array_push($out, $dict);
	}

	echo json_encode($out);
?>
