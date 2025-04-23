function updateCameraScreen(content) {
    console.log('Updating camera screen with content:', content);
    const cameraScreen = $('#camera-screen');
    cameraScreen.empty(); // Clear the current content

    // Add the background image
    const backgroundImage = $('<img>').attr('src', content.background.src).attr('alt', content.background.alt).addClass('camera-screen-img');
    cameraScreen.append(backgroundImage);

    // Add the title as an <h> element
    const title = $('<h>').text(content.title).addClass('camera-screen-title');
    cameraScreen.append(title);

    // Add a <div> for the content
    const contentDiv = $('<div>').addClass('camera-screen-text');
    // Loop through the content array and add elements based on type
    content.content.forEach(item => {
        if (item.type === 'text') {
            // Add text content in a <p> block
            const textElement = $('<p>').text(item.content);
            contentDiv.append(textElement);
        }
    });
    cameraScreen.append(contentDiv);

    // show camera screen
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
    // Initialize the counter
    let counter = 0;

    // Handle button click event
    $('#camera-shutter-button').on('click', function () {
        // Play a sound
        const audio = new Audio('/static/sounds/shutter_sound.mp3');
        audio.play();

        if (counter <= numberOfPages) {
            // Increment the counter
            counter++;
            console.log('Counter:', counter);
            if (counter <= numberOfPages) {
                // Make an AJAX request to the backend
                url = topic + '/' + counter;
                ajaxRequest(url);
            } else {
                // Show a message saying reaching the end of the content
                $('#camera-screen').empty(); // Clear the current content
                $('#camera-screen-default .camera-screen-text').empty();
                $('#camera-screen-default .camera-screen-text').append('<p>You have reached the end of the content.</p>');
                $('#camera-screen-default .camera-screen-text').append('<a href="/">Go back to the home page</a>');
                $('#camera-screen').hide(); // Hide the camera screen
            }
        }
    });

    $('#camera-playback-button').on('click', function () {
        // Play a sound
        const audio = new Audio('/static/sounds/playback_button_sound.mp3');
        audio.play();

        if (counter > 0) {
            // Decrease the counter
            counter--;
            console.log('Counter:', counter);
            if (counter > 0) {
                // Make an AJAX request to the backend
                url = topic + '/' + counter;
                ajaxRequest(url);
            } else {
                // TODO: Show a message saying reaching the beginning of the content
                $('#camera-screen').empty(); // Clear the current content
                $('#camera-screen-default .camera-screen-text').empty();
                $('#camera-screen-default .camera-screen-text').append('<p>You have reached the beginning of the content.</p>');
                $('#camera-screen').hide(); // Hide the camera screen
            }   
        }
    });
});