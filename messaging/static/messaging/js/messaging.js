// setting the href for the delete confirm modal
$(".call-delete").click(function(event) {
    event.preventDefault();
    var objectId = $(this).attr("data-messages");
    var deleteUrl = `/messaging/delete_thread/${objectId}/`

    $("#confirm-delete").attr("href", deleteUrl);
});
