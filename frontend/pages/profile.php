<?php
    $user = $usersystem->getUserInformation("username");
    $age = $usersystem->getUserInformation("age");
    $gender = $usersystem->getUserInformation("gender");
    $mothertongue = $usersystem->getUserInformation("mothertongue");

    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container">

	<div class="row row-spacing">
        <div class="col-xs-12 col-sm-4">
			<div class="profile-picture">
                <i class="fa fa-user" aria-hidden="true"></i>
			</div>
		</div>

		<div class="col-xs-12 col-sm-4">
			<div class="profile-information-title">
				Email
			</div>
			<div class="profile-information">
				<?php echo $user ?>
			</div>

            <div class="profile-information-title row-spacing">
				Age
			</div>
			<div class="profile-information">
				<?php echo $age ?>
			</div>
		</div>

        <div class="col-xs-12 col-sm-4">
			<div class="profile-information-title">
				Gender
			</div>
			<div class="profile-information">
				<?php echo $gender ?>
			</div>

            <div class="profile-information-title row-spacing">
				Mothertongue
			</div>
			<div class="profile-information">
				<?php echo $mothertongue ?>
			</div>
		</div>
	</div>

    <div class="row row-spacing">

	</div>

</div>
