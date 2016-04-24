<?php
    $user = $usersystem->getUserInformation("username");
    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container main-container">

    <div class="row">
        <div class="col-xs-12" id="avg-error-distr">
        
        </div>
    </div>

</div>

<script type="text/javascript" src="js/statistics/Statistics.js"></script>
<script type="text/javascript" src="js/statistics/display_statistics.js"></script>
