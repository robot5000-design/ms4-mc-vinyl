// Update quantity on click
$('.update-quantity').click(function(e) {
    var form = $(this).prev('.update-form');
    form.submit();
})
