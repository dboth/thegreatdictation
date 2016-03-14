<div class="container" id="analysis-container" hidden>

    <div class="row row-spacing text-center">
        <div class="col-xs-12">
            <a role="button" class="btn btn-primary" href="?p=dictation">Start a new dictation</a>
        </div>
    </div>

    <div class="row row-content row-spacing-lg" id="input-info">
        <div class="col-xs-12">
            <div class="subtitle title-hline">What you've entered</div>
            <div class="info-container error-indication" id="input-info-container">
            </div>
        </div>
    </div>

    <div class="row row-content row-spacing-lg" id="wordwise-legend">
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

    <div class="row row-content row-spacing-lg">
        <div class="col-xs-12 col-sm-8">
            <div class="subtitle title-hline">Error Distribution (Character-wise)</div>

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
            <div class="subtitle title-hline">Rating</div>

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

    <div class="row row-content row-spacing-lg">
        <div class="col-xs-12">
            <div class="subtitle title-hline">Detailed word by word error info</div>
        </div>
        <div class="col-xs-12" id="wordwise-error-info">
            <div class="row text-info">
                <div class="col-xs-5 col-sm-3">
                    Correct Spelling
                </div>

                <div class="hidden-xs col-sm-3">
                    Your Spelling
                </div>

                <div class="hidden-xs col-sm-2">
                </div>

                <div class="col-xs-7 col-sm-4">
                    Correction
                </div>
            </div>
        </div>
    </div>

    <div class="row row-content row-spacing-lg">
        <div class="col-xs-12">
            <div class="subtitle title-hline">Performance over time (word-wise)</div>
        </div>
        <div class="col-xs-12 ct-chart" id="performance-over-time-chart"></div>
    </div>

</div>
