<!doctype html>
<html lang="de">

<head>
	<title><tgd_title></title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />

	<!-- STYLESHEETS -->
	<link rel="stylesheet" href="css/font-awesome.min.css" />
	<link rel="stylesheet" href="css/tgd.css" />

	<!-- JAVASCRIPT -->
	<script src="js/jquery/jquery.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/libs/tinycolor/tinycolor.js"></script>
	<script src="js/libs/chartist.js"></script>

	<script src="js/error_handler.js"></script>
	<script src="js/functions.js"></script>
</head>

<body>
	<?php
		$user = $usersystem->getUserInformation("username");
	?>
    <!-- BEGIN: NAVIGATION BAR -->
		<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
			<div class="container">

				<div class="navbar-header">
					<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#tgd-main-nav" aria-expanded="false">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>

					<a class="navbar-brand" href="?p=home">TGD</a>
				</div>

				<div class="collapse navbar-collapse" id="tgd-main-nav">
					<ul class="nav navbar-nav">
						<li><a href="?p=getstarted">Get Started</a></li>
						<li><a href="?p=dictation">Dictation</a></li>
						<li><a href="?p=why">Why Dictation?</a></li>
						<li><a href="?p=aboutus">About Us</a></li>
                    </ul>

					<ul class="nav navbar-nav navbar-right">
						<?php

						if (!$user) {
							echo '<li><a data-toggle="modal" href="#login-modal"><i class="fa fa-sign-in"></i> Register or Log In</a></li>';
						} else {
							echo '<li><a href="#"><i class="fa fa-user"></i> '.$user.'</a></li>';
							echo '<li><a href="?logout"><i class="fa fa-sign-out"></i> Log Out</a></li>';
						}
						?>
						<li><a data-toggle="modal" href="#feedback-modal"><i class="fa fa-comment"></i> Send Feedback</a></li>
						<li><a href="?P=faq"><i class="fa fa-question-circle"></i> FAQ</a></li>
					</ul>
				</div>

			</div>
		</nav>
	<!-- END: NAVIGATION BAR -->

	<!-- BEGIN: MODALS -->
		<tgd_page>feedback_modal.html</tgd_page>

		<tgd_page>login_modal.html</tgd_page>
	<!-- END: MODALS -->

	<div id="wrapper">
		<div class="jumbotron">
			<div class="container">
				<div class="text-center jumbotron-header">
		            <h3><tgd_header-title></h3>
		        </div>

				<div class="jumbotron-content">
					<tgd_citation>
				</div>

			</div>
		</div>
		<!-- BODY -->
		<div id="content">
			<tgd_body>
		</div>

		<!-- FOOTER -->
		<footer class="page-footer">
			<div class="container">

				<div class="row row-content">
					<div class="col-xs-12 col-sm-4">
						I bin a geiler bock
					</div>

					<div class="col-xs-12 col-sm-4">
						AU REVOIR!
					</div>

					<div class="col-xs-12 col-sm-4">
						AU REVOIR!
					</div>
				</div>

			</div>
		</footer>

	</div>
</body>

</html>