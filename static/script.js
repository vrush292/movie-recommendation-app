$(document).ready(function() {
    $('#movieForm').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const movieTitle = $('#movieTitle').val(); // Get the movie title input
        $('.container').addClass('warp'); // Add the warp effect
        $('#loading').show(); // Show loading message
        $('#recommendations').hide(); // Hide recommendations initially
        $('#backBtn').hide(); // Hide back button

        // Make an AJAX request to fetch recommendations
        $.ajax({
            url: '/get_recommendations', // Adjust the URL according to your backend
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ title: movieTitle }), // Send the movie title as JSON
            success: function(data) {
                $('#loading').hide(); // Hide loading message
                $('#recommendations').empty().show(); // Clear and show recommendations container
                
                if (data.recommendations.length > 0) {
                    $('#recommendations').append('<h4>These are the recommendations :</h4>');
                    data.recommendations.forEach(function(movie) {
                        // Append each recommendation as a new item
                        $('#recommendations').append('<div class="recommendation-item">' + movie + '</div>');
                    });
                } else {
                    // Message when no recommendations are found
                    $('#recommendations').append('<div class="recommendation-item">No recommendations found.</div>');
                }
                
                // Hide the form and show the recommendations and back button
                $('#movieForm').hide(); // Hide the form
                $('#backBtn').show(); // Show back button
                $('.container').removeClass('warp'); // Remove the warp effect after loading
            },
            error: function() {
                $('#loading').hide(); // Hide loading message
                $('# recommendations').empty().show().append('<div class="recommendation-item">Error fetching recommendations. Please try again.</div>');
                $('#backBtn').hide();
                $('#movieForm').show(); // Show the form again in case of error
                $('.container').removeClass('warp'); // Ensure warp effect is removed on error
            }
        });
    });

    $('#backBtn').on('click', function() {
        $('#recommendations').hide(); // Hide recommendations
        $('#backBtn').hide(); // Hide back button
        $('#movieForm').show(); // Show the original form
        $('#movieTitle').val(''); // Clear the input field
    });
});