<?php
    $user = $usersystem->getUserInformation("username");
    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container main-container">
    <div class="row row-content">
		<div class="col-xs-12">
			<div class="row">
				<div class="col-xs-12 text-center title-description">
					Take a moment to
				</div>
			</div>

			<div class="row">
				<div class="col-xs-12 text-center title">
					Help us Evaluating this Service
				</div>
			</div>

			<div class="row">
				<div class="col-xs-12 text-center title-description">
					so we can improve it asap
				</div>
			</div>
		</div>
    </div>

	<div class="row row-content">
		<div class="col-xs-12">
			<form class="form-horizontal" id="eval-survey" action="sockets/sendSurvey.php">

				<!-- GET STARTED -->
				<div class="form-group row row-spacing">
					<div class="col-xs-12">
						<label for="getstarted-rating">Was Get Started helpful?</label>
					  		<fieldset id="getstarted-rating">
								<label for="gs-1"> 1 </label><input type="radio" name="getstarted-rating" id="gs-1" value="1" />
								<label for="gs-2"> 2 </label><input type="radio" name="getstarted-rating" id="gs-2" value="2" />
								<label for="gs-3"> 3 </label><input type="radio" name="getstarted-rating" id="gs-3" value="3" />
								<label for="gs-4"> 4 </label><input type="radio" name="getstarted-rating" id="gs-4" value="4" />
								<label for="gs-5"> 5 </label><input type="radio" name="getstarted-rating" id="gs-5" value="5" />
					  		</fieldset>

						<label for="getstarted-suggestions">Some suggested improvements?</label>
						<textarea class="form-control" name="getstarted-suggestions" id="getstarted-suggestions" placeholder="Type in your suggestions here" rows="5"></textarea>
					</div>
				</div>

				<!-- DICTATION PAGE -->
				<div class="form-group row row-spacing">
					<div class="col-xs-12">
						<label for="dictation-rating">Did you cope well with the main dictation site?</label>
					  		<fieldset id="dictation-rating">
								<label for="dictaion-1"> 1 </label><input type="radio" name="dictation-rating" id="dictaion-1" value="1" />
								<label for="dictaion-2"> 2 </label><input type="radio" name="dictation-rating" id="dictaion-2" value="2" />
								<label for="dictaion-3"> 3 </label><input type="radio" name="dictation-rating" id="dictaion-3" value="3" />
								<label for="dictaion-4"> 4 </label><input type="radio" name="dictation-rating" id="dictaion-4" value="4" />
								<label for="dictaion-5"> 5 </label><input type="radio" name="dictation-rating" id="dictaion-5" value="5" />
					  		</fieldset>

						<label for="dictation-suggestions">Some suggested improvements?</label>
						<textarea class="form-control" name="dictation-suggestions" id="dictation-suggestions" placeholder="Type in your suggestions here" rows="5"></textarea>
					</div>
				</div>

				<!-- BACKGROUND INFOS ABOUT DICTATION -->
				<div class="form-group row row-spacing">
					<div class="col-xs-12">
						<label for="background-rating">Did you like the infos about dictation background ("Why Dictation")?</label>
					  		<fieldset id="background-rating">
								<label for="background-1"> 1 </label><input type="radio" name="background-rating" id="background-1" value="1" />
								<label for="background-2"> 2 </label><input type="radio" name="background-rating" id="background-2" value="2" />
								<label for="background-3"> 3 </label><input type="radio" name="background-rating" id="background-3" value="3" />
								<label for="background-4"> 4 </label><input type="radio" name="background-rating" id="background-4" value="4" />
								<label for="background-5"> 5 </label><input type="radio" name="background-rating" id="background-5" value="5" />
					  		</fieldset>

						<label for="background-suggestions">Some suggested improvements?</label>
						<textarea class="form-control" name="background-suggestions" id="background-suggestions" placeholder="Type in your suggestions here" rows="5"></textarea>
					</div>
				</div>

				<!-- Would You Use -->
				<div class="form-group row row-spacing">
					<div class="col-xs-12">
						<label for="wouldyouuse-rating">Would you use this platform for language learning?</label>
					  		<fieldset id="wouldyouuse-rating">
								<label for="wouldyouuse-1"> 1 </label><input type="radio" name="wouldyouuse-rating" id="wouldyouuse-1" value="1" />
								<label for="wouldyouuse-2"> 2 </label><input type="radio" name="wouldyouuse-rating" id="wouldyouuse-2" value="2" />
								<label for="wouldyouuse-3"> 3 </label><input type="radio" name="wouldyouuse-rating" id="wouldyouuse-3" value="3" />
								<label for="wouldyouuse-4"> 4 </label><input type="radio" name="wouldyouuse-rating" id="wouldyouuse-4" value="4" />
								<label for="wouldyouuse-5"> 5 </label><input type="radio" name="wouldyouuse-rating" id="wouldyouuse-5" value="5" />
					  		</fieldset>

						<label for="wouldyouuse-suggestions">If not, why?</label>
						<textarea class="form-control" name="wouldyouuse-suggestions" id="wouldyouuse-suggestions" placeholder="Type in your suggestions here" rows="5"></textarea>
					</div>
				</div>

				<!-- Learning as a game -->
				<div class="form-group row row-spacing">
					<div class="col-xs-12">
						<label for="learninggame-rating">Would you like dictation as kind of a game (e.g. colegting points and challenges)?</label>
					  		<fieldset id="learninggame-rating">
								<label for="learninggame-1"> 1 </label><input type="radio" name="learninggame-rating" id="learninggame-1" value="1" />
								<label for="learninggame-2"> 2 </label><input type="radio" name="learninggame-rating" id="learninggame-2" value="2" />
								<label for="learninggame-3"> 3 </label><input type="radio" name="learninggame-rating" id="learninggame-3" value="3" />
								<label for="learninggame-4"> 4 </label><input type="radio" name="learninggame-rating" id="learninggame-4" value="4" />
								<label for="learninggame-5"> 5 </label><input type="radio" name="learninggame-rating" id="learninggame-5" value="5" />
					  		</fieldset>

						<label for="learninggame-suggestions">Some inspiring ideas?</label>
						<textarea class="form-control" name="learninggame-suggestions" id="learninggame-suggestions" placeholder="Type in your suggestions here" rows="5"></textarea>
					</div>
				</div>

				<div class="form-group row row-spacing">
					<div class="col-xs-12">
						<label for="getstarted-suggestions">Further improvement suggestions?</label>
						<textarea class="form-control" id="further-suggestions" name="further-suggestions" placeholder="Type in your suggestions here" rows="5"></textarea>
					</div>
				</div>

				<div class="form-group row row-spacing">
					<div class="col-xs-12">
						<button type="submit" class="btn btn-primary" name="survey">Submit your Answers</button>
					</div>
				</div>

			</form>
		</div>
	</div>
</div>
