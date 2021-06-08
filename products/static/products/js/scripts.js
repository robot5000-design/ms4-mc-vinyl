$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
})

$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();
    if(selectedVal != "reset"){
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
})

// Disable +/- buttons outside 1-99 range
function handleEnableDisable(itemId) {
    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 98;
    $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

// Ensure proper enabling/disabling of all inputs on page load
var allQtyInputs = $('.qty_input');
for(var i = 0; i < allQtyInputs.length; i++){
    var itemId = $(allQtyInputs[i]).data('item_id');
    handleEnableDisable(itemId);
}

// Check enable/disable every time the input is changed
$('.qty_input').change(function() {
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
});

// Increment quantity
$('.increment-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue + 1);
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
});

// Decrement quantity
$('.decrement-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue - 1);
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
});

$(".call-delete").click(function(event) {
    event.preventDefault();
    var productId = $(this).attr("data-product");
    var deleteUrl = `/products/delete/${productId}/`
    $("#confirm-delete").attr("href", deleteUrl);
});

$('#new-image').change(function() {
    var file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
});

window.addEventListener("load", function() {
    function a(a) {
        a.querySelectorAll(".remove").forEach(a=>{
            a.addEventListener("click", ()=>{
                a.parentNode.remove()
            }
            )
        }
        )
    }
    function b(b) {
        const d = b.querySelector(".array-item")
        , e = d.cloneNode(!0)
        , f = d.parentElement;
        d.getAttribute("data-isNone") && (d.remove(),
        e.removeAttribute("data-isNone"),
        e.removeAttribute("style")),
        a(b),
        b.querySelector(".add-array-item").addEventListener("click", ()=>{
            c++;
            const b = e.cloneNode(!0)
            , d = b.querySelector("input").getAttribute("id").split("_")
            , g = d.slice(0, -1).join("_") + "_" + (c - 1 + "");
            b.querySelector("input").setAttribute("id", g),
            b.querySelector("input").value = "",
            a(b),
            f.appendChild(b)
        }
        )
    }
    let c = 1;
    $(".dynamic-array-widget").not(".empty-form .dynamic-array-widget").each((a,c)=>b(c)),
    $(document).on("formset:added", function(a, c) {
        c[0].querySelectorAll(".dynamic-array-widget").forEach(a=>b(a))
    })
});
