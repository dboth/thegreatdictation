<?php
    $user = $usersystem->getUserInformation("username");
    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container main-container">

    <div class="row">
        <div class="col-xs-12 col-sm-6">
            <div class="subtitle">
                Average Error Distribution
            </div>

            <div class="row-spacing" id="avg-error-distr">

            </div>
        </div>

        <div class="col-xs-12 col-sm-6">
            <div class="subtitle">
                Performance
            </div>

            <div class="row-spacing text-center" id="avg-score">

            </div>

            <div class="row-spacing text-center" id="min-score">

            </div>

            <div class="row-spacing text-center" id="max-score">

            </div>
        </div>
    </div>

</div>

<script type="text/javascript" src="js/statistics/Statistics.js"></script>
<script type="text/javascript" src="js/statistics/display_statistics.js"></script>
