<?php
    $user = $usersystem->getUserInformation("username");
    if (!$user) {
        header('Location: ?p=register');
        exit;
    }
?>

<div class="container">

    <div class="row row-content">

        <div class="col-xs-12 text-center analysis-swapper">
            <a class="active" id="dict-switch">Dictation</a> / <a id="res-switch">Result</a>
        </div>

    </div>
</div>

<div class="container" id="loading-container">
    <div class="row row-content">
        <div class="col-xs-12" id="loading-bar">

        </div>
    </div>
</div>

<div class="container main-container" id="dictation-container">
    <form action="<tgd_analysispath>" method="POST" id="dictation-form">
        <div class="row row-content">
            <div class="col-xs-12 explanation">
                <label>How to</label>
                <ul>
                    <li>Choose a text to start and confirm your choice</li>
                    <li>Listen to the whole audio and Write down all sentences</li>
                </ul>
            </div>
        </div>

        <div class="row row-content">

            <label for="dictation-id" class="control-label col-xs-3 col-sm-1 ">Choose</label>
            <div class="col-xs-9 col-sm-3 ">
                <select class="form-control" id="dictation-id" name="subject">
                    <tgd_texts>
                </select>
            </div>

            <div class="col-xs-12 col-sm-2 text-center ">
                <button class="btn btn-primary" id="select-text-button">Select this text</button>
            </div>

            <div class="col-xs-12 col-sm-6  text-right" id="audio-player-col">

            </div>

        </div>

        <div class="row row-content">

            <div class="col-xs-12">

                <div class="form-group">
                    <label for="data">What you understand</label>
                    <textarea  class="form-control" rows="10" placeholder="Choose a text first!" id="dictation-text" name="data" disabled>
                        Liebe Tonia, kannewst du bitte einufen? Ich habe heute Nacmhittag keine Zeit und ich möchte heute Abend kochen. I ch brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. das Für Frühstück brauchen Tee, Kaffee, Brot, ButterMarmelade, Käse und Wurst. Kwe annst du auch Schokolade und Coka mitbringen? Viele Dank! Liebe Grüße Mama
                    </textarea>
                </div>

                <div class="text-center">
                    <button type="submit" class="btn btn-primary" id="dictation-submit" disabled>Finish Dictation</button>
                </div>

            </div>

        </div>
    </form>
</div>

<div class="container" id="analysis-container" hidden>

    <div class="row row-spacing text-center">
        <div class="col-xs-12 text-center">
            This was your <span class="pointout-font"><?php echo $usersystem->getResultCount() + 1 ?>.</span> dictation! <br />
            You are awesome!
        </div>
        <div class="col-xs-12 row-spacing">
            <a role="button" class="btn btn-primary" href="?p=dictation">Start a new dictation</a>
        </div>
    </div>

    <tgd_result>

</div>

<script src="js/result_generation/result_components.js"></script>
<script src="js/result_generation/create_analysis.js"></script>
<script src="js/page_events/handle_dictation.js"></script>
<script src="js/async_calls/call_audio_path.js"></script>
