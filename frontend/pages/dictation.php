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

            <label for="dictation-id" class="control-label col-xs-3 col-sm-1 col-content">Choose</label>
            <div class="col-xs-9 col-sm-3 col-content">
                <select class="form-control" id="dictation-id" name="subject">
                    <tgd_texts>
                </select>
            </div>

            <div class="col-xs-12 col-sm-2 text-center col-content">
                <button class="btn btn-primary" id="select-text-button">Select this text</button>
            </div>

            <div class="col-xs-12 col-sm-6 col-content text-right" id="audio-player">

            </div>

        </div>

        <div class="row row-content">

            <div class="col-xs-12">

                <div class="form-group">
                    <label for="data">What you understand</label>
                    <textarea  class="form-control" rows="10" placeholder="Choose a text first!" id="dictation-text" name="data" disabled>Ich bin ein Elefant</textarea>
                </div>

                <div class="text-center">
                    <button type="submit" class="btn btn-primary" id="dictation-submit" disabled>Finish Dictation</button>
                </div>

            </div>

        </div>
    </form>
</div>

<div class="container" id="analysis-container" hidden>

    <div class="row row-content" id="input-info">
        <div class="col-xs-12">
            <div class="subtitle">What you've entered</div>
            <div class="info-container error-indication" id="input-info-container">
            </div>
        </div>
    </div>

    <div class="row row-content" id="wordwise-legend">
        <div class="col-xs-12 text-center">
            <div class="legend">
                <div class="element missing-word">
                    Missing Word
                </div>
                <div class="element wrong">
                    Wrong Word/spelling
                </div>
                <div class="element minor-mistake">
                    Minor spelling mistake
                </div>
            </div>
        </div>
    </div>

    <div class="row row-content">
        <div class="col-xs-12 col-sm-8">
            <div class="subtitle">Error Distribution (Character-wise)</div>
            <div class="ct-chart ct-minor-seventh" id="error-distribution-chart"></div>

            <div class="row" id="charwise-legend">
                <div class="col-xs-12 text-center">
                    <div class="legend">
                        <div class="element substitution">
                            Wrong Letter
                        </div>
                        <div class="element insertion">
                            Missing Letter
                        </div>
                        <div class="element deletion">
                            Waste Letter
                        </div>
                        <div class="element punctuation">
                            Punctuation Mistake
                        </div>
                        <div class="element switch">
                            Switched Letters
                        </div>
                        <div class="element capitalization">
                            Capitalization Mistake
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="col-xs-12 col-sm-4">
            <div class="subtitle">Rating</div>

            <div class="row" id="score-info">
                <div class="col-xs-12">
                    <label>Correct words</label>
                    <div class="ratio"></div>
                </div>

                <div class="col-xs-12">
                    <label>Your score</label>
                    <div class="score"></div>
                </div>
            </div>
        </div>
    </div>

    <div class="row row-content">

        <div class="col-xs-12 subtitle">Performance over time (word-wise)</div>
        <div class="col-xs-12 ct-chart" id="performance-over-time-chart">

        </div>
    </div>

    <div class="row row-content">
        <div class="col-xs-12 subtitle">Detailed word by word error info</div>
        <div class="col-xs-12" id="wordwise-error-info">

        </div>
    </div>

</div>

<script src="js/result_generation/result_components.js"></script>
<script src="js/result_generation/create_analysis.js"></script>
<script src="js/page_events/handle_dictation.js"></script>
<script src="js/async_calls/call_audio_path.js"></script>
