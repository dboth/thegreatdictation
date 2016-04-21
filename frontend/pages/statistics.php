<?php
    $user = $usersystem->getUserInformation("username");
    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container">
	
</div>
