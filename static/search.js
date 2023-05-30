function searchPasswordManager() {
    var formData = $('#password-manager-form').serialize();
    $.ajax({
        type: 'POST',
        url: '/submit_form',
        data: formData,
        dataType: 'json',
        success: function(data) {
            // Update the HTML elements with the search results
            $('#search-results').html(data.html);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Error searching password managers: ' + textStatus);
        }
    });
}