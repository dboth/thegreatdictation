<?php
    $user = $usersystem->getUserInformation("username");
    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container">

	<div class="row row-spacing">
		<div class="col-xs-12 col-sm-6">
			<div class="profile-information-title">
				Email
			</div>
			<div class="profile-information">
				<?php echo $user ?>
			</div>
		</div>

		<div class="col-xs-12 col-sm-6">

		</div>
	</div>

</div>
