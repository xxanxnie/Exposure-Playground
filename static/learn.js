function updateCameraScreen(content) {
	console.log('Updating camera screen with content:', content);
	const cameraScreen = $('#camera-screen');
	cameraScreen.empty(); // Clear the current content

	// Add the background image
	const backgroundImage = $('<img>')
		.attr('src', content.background.src)
		.attr('alt', content.background.alt)
		.addClass('camera-screen-img');
	cameraScreen.append(backgroundImage);

	// Add the title as an <h> element
	const title = $('<h>').text(content.title).addClass('camera-screen-title');
	cameraScreen.append(title);

	// Add a <div> for the animated content
	const contentDiv = $('<div>').addClass('camera-screen-text');
	cameraScreen.append(contentDiv);

	let paragraphIndex = 0;

	function typeParagraph() {
		if (paragraphIndex >= content.content.length) return;

		const item = content.content[paragraphIndex];
		if (item.type !== 'text') {
			paragraphIndex++;
			typeParagraph();
			return;
		}

		const paragraph = $('<p></p>').appendTo(contentDiv);
		let charIndex = 0;
		const text = item.content;

		function typeChar() {
			if (charIndex < text.length) {
				paragraph.append(text.charAt(charIndex));
				charIndex++;
				setTimeout(typeChar, 50); // typing speed, 50 = medium
			} else {
				paragraphIndex++;
				setTimeout(typeParagraph, 300); // delay before next paragraph
			}
		}

		typeChar();
	}

	typeParagraph();
	$('#camera-screen').show();
}

function ajaxRequest(url) {
	$.ajax({
		url: url,
		method: 'GET',
		success: function (response) {
			updateCameraScreen(response);
		},
		error: function (xhr, status, error) {
			console.error('Error fetching content:', error);
		}
	});
}

$(document).ready(function () {
	let counter = 0;

	// Retrieve progress from sessionStorage
    const progressKey = `learning_progress_${topic}`;
    const savedProgress = sessionStorage.getItem(progressKey);
	if (savedProgress && !isNaN(savedProgress) && savedProgress > 0) {
        counter = parseInt(savedProgress, 10);
        console.log('Resuming progress at page:', counter);
        url = topic + '/' + counter;
        ajaxRequest(url);
    }

	// Handle button click event
	$('#camera-shutter-button').on('click', function () {
		// Play sound effect
		const audio = new Audio('/static/sounds/shutter_sound.mp3');
		audio.play();

		if (counter <= numberOfPages) {
			counter++;
			console.log('Counter:', counter);
			if (counter <= numberOfPages) {
				// Save progress to sessionStorage
				sessionStorage.setItem(progressKey, counter);
				// Make AJAX request to the backend
				url = topic + '/' + counter;
				ajaxRequest(url);
			} else {
				// Show a message saying reaching the end of the content
				$('#camera-screen').empty();
				$('#camera-screen-default .camera-screen-text').empty();
				$('#camera-screen-default .camera-screen-text').append('<p class="mb-3">You have reached the end of the content!</p>');


				$('#camera-screen-default .camera-screen-text').append(`
					<a href="/interact/shutter" class="btn btn-success mb-3 w-100">🚀 Launch Camera Playground</a>
				`);
				let quizRoute = `/quiz_${topic}/1`;
				$('#camera-screen-default .camera-screen-text').append(`
					<a href="${quizRoute}" class="btn btn-primary mb-3 w-100">📝 Take the Quiz</a>
				`);
				$('#camera-screen-default .camera-screen-text').append(`
					<a href="/" class="btn btn-outline-secondary mb-3 w-100">🏠 Go Back to Home</a>
				`);

				$('#camera-screen').hide();
			}
		}
	});

	$('#camera-playback-button').on('click', function () {
		// Play a sound
		const audio = new Audio('/static/sounds/playback_button_sound.mp3');
		audio.play();

		if (counter > 0) {
			counter--;
			console.log('Counter:', counter);
			if (counter > 0) {
				// Save progress to sessionStorage
				sessionStorage.setItem(progressKey, counter);
				// Make AJAX request to the backend
				url = topic + '/' + counter;
				ajaxRequest(url);
			} else {
				$('#camera-screen').empty(); // Clear current content
				$('#camera-screen-default .camera-screen-text').empty();
				$('#camera-screen-default .camera-screen-text').append('<p>You have reached the beginning of the content.</p>');
				$('#camera-screen').hide(); // Hide camera screen
			}
		}
	});
});