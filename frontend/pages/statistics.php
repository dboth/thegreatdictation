<?php
    $user = $usersystem->getUserInformation("username");
    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container main-container">

</div>

<script type="text/javascript" src="js/statistics/Statistics.js"></script>
<script type="text/javascript" src="js/statistics/display_statistics.js"></script>
