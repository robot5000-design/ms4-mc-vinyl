// setting the href for the delete confirm modal
$(".call-delete").click(function(event) {
    event.preventDefault();
    var objectId = $(this).attr("data-messages");
    var deleteUrl = `/messaging/delete_thread/${objectId}/`;

    $("#confirm-delete").attr("action", deleteUrl);
});

// Show open threads only
$('.open-threads-btn').on('click', function() {
    $('.open-threads').show();
    $('.closed-threads').hide();
});

// Show closed threads only
$('.closed-threads-btn').on('click', function() {
    $('.closed-threads').show();
    $('.open-threads').hide();
});
