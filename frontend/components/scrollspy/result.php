<?php

$ids = array(
	"input-row" => "What you've entered" ,
	"errordistribution-row" => "Error Distribution",
	"score-row" => "Score",
	"charwise-row" => "Charwise Error Info",
	"performance-row" => "Performance over Time"
);

?>

<div class="sidebar affix hidden-xs hidden-print" data-offset-top="277" data-spy="affix" id="nav-scrollspy">
	<ul class="nav nav-tabs nav-stacked" role="tablist">
		<?php foreach ($ids as $id => $title) {
			echo "<li><a href='#".$id."'>".$title."</a></li>";
		} ?>
	</ul>
</div>
