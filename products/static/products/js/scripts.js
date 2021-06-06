$(".call-delete").click(function(event) {
    event.preventDefault();
    var productId = $(this).attr("data-product");
    var deleteUrl = `/products/delete/${productId}/`
    $("#confirm-delete").attr("href", deleteUrl);
});
