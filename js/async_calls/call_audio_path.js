$(document).ready(function() {
	$("#select-text-button").click(function(event) {
		event.preventDefault();

		var text_id = $("#dictation-id").val();

		console.log(text_id);

		if (!text_id) {
			requestErrorInfo("f_select_a_text");
		} else {
			$.ajax({
				url: "sockets/getAudioFile.php",
				type: 'POST',
				data: {"text_id": text_id}
			})
			.done(function(res) {
				// create audio
				var src = $("<source>").attr({
					src: 'src/audio/'+res,
					type: 'audio/wav'
				});

				var audio = $("<audio>").prop("controls", true)
				console.log("audio: "+audio);
				audio.html(src);
				$("#audio-player").append(audio);
			})
			.fail(function(res) {
				console.log("error", res);
			})
			.always(function() {
				console.log("complete");
			});
		}
	});

});
