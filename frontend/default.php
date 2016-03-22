<?php
	$user = $usersystem->getUserInformation("username");
?>

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
	<script src="js/libs/bootstrap-select.js"></script>

	<script src="js/error_handler.js"></script>
	<script src="js/functions.js"></script>
</head>

<body>
    <!-- BEGIN: NAVIGATION BAR -->
		<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
			<div class="container">

				<div class="navbar-header">
					<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#tgd-main-nav" aria-expanded="false">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>

					<a class="navbar-brand" href="?p=home"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC40lEQVRYR+2WTUhUURTH/+c5jDMlgkFFkURIWomS780bmzYZCNGHLQJDMiKiRUQtIiIIatUqKtpa2KKPRdgi6WsRFkUhzbz7jBnsayHURinCxWSZw5t/XHHChpxxxgk3Pnhc5s49//O755x73hXM8yPz7B8LAAsRKCgC4XC41vO8DQDqSNaKSN1UEb8H8J6kfhMDAwOfZlvcswJobm5enkqlrohIxyyE0wCuTkxMnEkkEqP51ucFME3zoIhcBlCVTyzr/68kj7uueyeXXU6ApqamiGEYr4Cij2sKgKWUSswEMSNAe3t72dDQkANgY4E7/2s5yVhNTU2kp6fH+5fOjACWZe0DcHsuzjO2JDtmSkUugIsATpYI4ILruqcLjcBDADtKAQDggVKqrVCAQQD6zJfieauUqi8UQDeXTKOZK8QHpdS6ggBM02wTkQMAdgIIFkmQFJG7JK8rpV7mBAiHw2s8z9tLclBEniqlfmiDxsbGxX6/fzvJrQC2TKUlV/94B+AZyb7y8vLH/f39PwEYtm2vJ7mJ5FoReeE4ziOtPylkWdYlACemNZxfAPpI3isrK7sfi8VGMvQNDQ1VgUBgNckVAFZOzQ8DGDYM43M0Gv2m5+rr6/3BYLCV5B4AuwEsnR4Bkl2u6x4R27Zb0+n0kxwhJoDXIqJ3NkxyREQmR/1bRHwiUu153io9AqjWI8nNACrzpG6bWJZ1C0BnkTmeq1mvmKbZLSKH5qpUpH23jsBhANdyCHwUkSjJNyIS9zzvi4iM6TcQCHzXduPj4xWe51X4fL4KnQKSli4tABEAS3Jod04WYSgUuklyf9bCuIiccxynt8jd6eJeBOAogFMAlmXpnFdKnZ0EiEQiQX2BAKBToSt7NJVKVcfj8bFinU+3s23bTqfTUT2nv46GYXQ5jtP95xhmFre0tPiSyeQuEal0HOdGKZxnNEKh0DGSz7PvBnlvRKWEKKgV/2/HGf2FCCxE4DedqhWAqUhAMQAAAABJRU5ErkJggg==" alt="TGD Icon" /></a>
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
							echo '<li><a data-toggle="modal" href="#login-modal"><i class="fa fa-sign-in"></i> Sign In</a></li>';
						} else {
							echo '<li><a href="#"><i class="fa fa-user"></i> '.$user.'</a></li>';
							echo '<li><a href="?logout"><i class="fa fa-sign-out"></i> Log Out</a></li>';
						}
						?>
						<li><a data-toggle="modal" href="#feedback-modal"><i class="fa fa-comment"></i> Feedback</a></li>
						<!--<li><a href="?P=faq"><i class="fa fa-question-circle"></i> FAQ</a></li>-->
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
			<div class="container">

				<?php

				if ($usersystem->getResultCount() >= 3) {
					echo '
					<div class="text-center alert alert-success" role="alert">
						<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						You have already finished '.$usersystem->getResultCount().' dictations! Thank you for your help. If you could evaluate your work, this would help us even more!<br />
						<a class="alert-link" href="?p=survey">Take the survey now!</a>
					</div>
					';
				}

				?>

			</div>
			<tgd_body>
		</div>

		<!-- FOOTER -->
		<footer class="page-footer">
			<div class="container">
				<div class="row">
					<div class="col-xs-12 col-sm-4">
						<div class="title-small">
							Sitemap
						</div>
						<a href="?p=home">Startpage</a> <br />
						<a href="?p=getstarted">Get Started</a> <br />
						<a href="?p=why">Why Dictation</a> <br />
						<a href="?p=aboutus">About Us</a> <br />
						<a href="?p=impressum">Impressum</a> <br />
						<a href="?p=contact">Contact us</a>
					</div>

					<div class="col-xs-12 col-sm-4">
						<div class="title-small">
							Data Collection
						</div>
						<a href="?p=getstarted">Get Started</a> <br />
						<a href="?p=dictation">Dictation</a> <br />
						<a href="?p=survey">Survey</a> <br />
					</div>

					<div class="col-xs-12 col-sm-4">

					</div>
				</div>

			</div>
		</footer>

	</div>

</body>

</html>
