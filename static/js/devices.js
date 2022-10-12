//Remove files using Ajax
function delete_device(id) {
    $.ajax({
        url: "/delete/device/" + id,
        dataType: "json",
        type: "Post",
        async: true,
        success: function (response, textStatus, jqXHR) {
            document.getElementById(id).remove();
            var messageDiv = document.getElementById("message");
            messageDiv.className = "alert alert-success";
            messageDiv.textContent = "Dispositivo eliminado correctamente.";
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(textStatus)
            var messageDiv = document.getElementById("message");
            messageDiv.className = "alert alert-danger";
            messageDiv.textContent = "Error: no se ha podido eliminar el dispositivo.";
        }
    });
}