window.onload = function() {
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = JSON.stringify(form.serializeArray());
        $.ajax({
            type: "POST",
            url: "/recruiterRegistration",
            data: formData,
            dataType: "json",
            success: function(data, textStatus) {
                if (data.redirect) {
                    // data.redirect contains the string URL to redirect to
                    window.location.href = data.redirect;
                }
                else {
                    // data.form contains the HTML for the replacement form
                    $("#myform").replaceWith(data.form);
                }
            }
        });
    });
}
