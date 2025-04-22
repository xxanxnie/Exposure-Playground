$(document).ready(function () {
    // Initialize the counter
    let counter = 0;

    // Handle button click event
    $('#camera-shutter-button').on('click', function () {
        // Play a sound
        const audio = new Audio('/static/sounds/shutter_sound.mp3');
        audio.play();

        // Increment the counter
        counter++;
        console.log('Counter:', counter);

        // Make an AJAX request to the backend
        // $.ajax({
        //     url: '/get-content', // Replace with the correct backend endpoint
        //     method: 'POST',
        //     contentType: 'application/json',
        //     data: JSON.stringify({ counter: counter, lesson_id: lessonId }),
        //     success: function (response) {
        //         // Handle the response (e.g., update the page with new content)
        //         console.log('Content received:', response);
        //         $('#content-container').html(response.content); // Update a container with the new content
        //     },
        //     error: function (xhr, status, error) {
        //         console.error('Error fetching content:', error);
        //     }
        // });
    });
});