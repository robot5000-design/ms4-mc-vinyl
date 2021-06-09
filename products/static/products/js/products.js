$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
})

// change the sort dropdown to match the current chosen option
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

// setting the href for the delete confirm modal
$(".call-delete").click(function(event) {
    event.preventDefault();
    var productId = $(this).attr("data-product");
    var deleteUrl = `/products/delete/${productId}/`
    $("#confirm-delete").attr("href", deleteUrl);
});

// listen for image field change in product management form
$('#new-image').change(function() {
    var file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
});

// for the dynamic array for track listing
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
