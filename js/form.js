window.onload = function() {
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = JSON.stringify(form.serializeArray());
        $.ajax({
            type: "POST",
            data: formData,
            dataType: "json",
            success: function(data, textStatus) {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else if (data.error) {
                    var msg = document.createElement("p")
                    msg.setAttribute("style", "color: red")
                    msg.appendChild(document.createTextNode(data.error))
                    $("#loginForm").append(msg)
                } else if (data.response) {
                    var msg = document.createElement("p")
                    msg.appendChild(document.createTextNode(data.response))
                    $("#loginForm").append(msg)
                }
            }
        });
    });
}
