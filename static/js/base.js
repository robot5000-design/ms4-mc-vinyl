/**
 * When the go-back button is clicked the browser returns to the
 * previous page in history
 */
 function goBack() {
    window.history.back();
}

// Call the goBack function which goes back to the previous page in history
$(".go-back").click(goBack);

// show toasts
$('.toast').toast('show');

// back to top button
$(".btt-link").click(function(e) {
    window.scrollTo(0,0);
});

// Disable form submit button to prevent multiple entries and add overlay
$(".add-message-form").on("submit", function() {
    $(".add-message-btn").prop("disabled", "true");
    $('#loading-overlay').fadeToggle(4000);
});

// Add loading spinner to search site form submit
$(".search-site-form").submit(function() {
    $('#loading-overlay').fadeToggle(4000);
});

// Disable +/- buttons outside 1-99 range
function handleEnableDisable(itemId, currentValue) {
    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 98;
    $(`form #decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`form #mobile-decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`form #increment-qty_${itemId}`).prop('disabled', plusDisabled);
    $(`form #mobile-increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

// Ensure proper enabling/disabling of all inputs on page load
var allQtyInputs = $('.qty_input');
for(var i = 0; i < allQtyInputs.length; i++){
    var itemId = $(allQtyInputs[i]).data('item_id');
    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
    var mobileCurrentValue = parseInt($(`#mobile_id_qty_${itemId}`).val());
    handleEnableDisable(itemId, currentValue);
    handleEnableDisable(itemId, mobileCurrentValue);
}

// Check enable/disable every time the input is changed
$('.qty_input').change(function() {
    var itemId = $(this).data('item_id');
    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
    var mobileCurrentValue = parseInt($(`#mobile_id_qty_${itemId}`).val());
    handleEnableDisable(itemId, currentValue);
    handleEnableDisable(itemId, mobileCurrentValue);
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
