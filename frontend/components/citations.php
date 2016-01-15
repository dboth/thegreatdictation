<?php

$all_quotes = array(
	array('"We have two ears and one mouth, so we should listen more than we say."', 'Zeno of Citium, greek thinker/philosopher'),
	array('"Success is not final, failure is not fatal: it is the courage to continue that counts"', 'Winston Churchill, former british prime minister and Nobel Prize winner'),
	array('"You can\'t fake listening. It shows!"', 'Raquel Welch, actress and singer'),
	array('"There is a lot of difference between listening and hearing"', 'G.K. Chesterton, i.a. writer, poet, philospher, journalist'),
	array('"The art of conversation lies in listening"', 'Malcom Forbes, publisher of \'Forbes Magazine\'')
);

$quote = $all_quotes[array_rand($all_quotes)];

?>

<div class="text-center">
	<p class="quote">
	<i><b><?php echo $quote[0] ?></b> <br><?php echo $quote[1] ?></i>
	</p>
</div>
