const button = document.getElementById('click_to_convert');

var speech = false; // Initialize speech to false initially
var recognition;

button.addEventListener('click', function() {
    if (!speech) { // If speech is false, start recording
        speech = true;
        window.SpeechRecognition = window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.interimResults = true;

        recognition.addEventListener('result', e => {
            const transcript = Array.from(e.results)
                .map(result => result[0])
                .map(result => result.transcript);

            convert_text.innerHTML = transcript;
        });

        recognition.start();
        button.innerHTML = "Stop Recording"; // Change button text
    } else { // If speech is true, stop recording
        speech = false;
        recognition.stop();
        button.innerHTML = "Start Recording"; // Change button text
    }
});

