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
                } else if (data.response) {
                    var msg = document.createElement("p")
                    msg.appendChild(document.createTextNode(data.response))
                    $("#loginForm").append(msg)
                }
            }
        });
    });
}
