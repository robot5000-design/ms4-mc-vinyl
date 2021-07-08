// show toasts
$('.toast').toast('show');

// back to top button
$(".btt-link").click(function(e) {
    window.scrollTo(0,0);
});

// Disable form submit button to prevent multiple entries
$(".add-message-form").on("submit", function() {
    $(".add-message-btn").prop("disabled", "true");
});

// Disable +/- buttons outside 1-99 range
function handleEnableDisable(itemId, currentValue) {
    var currentValue = currentValue;
    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 98;
    $(`form #decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`form #increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

// Ensure proper enabling/disabling of all inputs on page load
var allQtyInputs = $('.qty_input');
for(var i = 0; i < allQtyInputs.length; i++){
    var itemId = $(allQtyInputs[i]).data('item_id');
    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
    handleEnableDisable(itemId, currentValue);
}

// Check enable/disable every time the input is changed
$('.qty_input').change(function() {
    var itemId = $(this).data('item_id');
    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
    console.log(currentValue)
    handleEnableDisable(itemId, currentValue);
});

// Increment quantity
$('.increment-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    if (currentValue < 99) {
        $(closestInput).val(currentValue + 1);
    }
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId, currentValue += 1);
});

// Decrement quantity
$('.decrement-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    if (currentValue > 1) {
        $(closestInput).val(currentValue - 1);
    }
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId, currentValue -= 1);
});

// Remove item from wishlist and reload on click
$('.wishlist-remove').click(function(e) {
    $(this).prop("disabled", true);
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var itemId = $(this).attr('id').split('remove_')[1];
    var url = `/wishlist/remove/${itemId}/`;
    var data = {
        'csrfmiddlewaretoken': csrfToken
    }

    $.post(url, data)
        .done(function() {
            location.reload();
        });
});