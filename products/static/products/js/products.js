// disable buttons after various form submission to prevent multiple submissions
$(".edit-review-form").on("submit", function() {
    $(".edit-review-btn").prop("disabled", "true");
    $('#loading-overlay').fadeToggle(4000);
});

$(".add-review-form").on("submit", function() {
    $(".add-review").prop("disabled", "true");
    $('#loading-overlay').fadeToggle(4000);
});

$(".add-cart-form").on("submit", function() {
    $(".add-cart-btn").prop("disabled", "true");
});

$(".add-product-form").on("submit", function() {
    $(".add-product-btn").prop("disabled", "true");
    $('#loading-overlay').fadeToggle(4000);
});

$("#confirm-delete").on("click", function() {
    $(this).addClass("disable-element");
});

// Upvote a Review
$('#upvote-review').click(function() {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var itemId = $(this).attr('data-items').split('_');
    var url = `/products/upvote_review/${itemId[0]}/${itemId[1]}/`;
    var data = {'csrfmiddlewaretoken': csrfToken};

    $.post(url, data)
     .done(function() {
         location.reload();
     });
})

// change the sort dropdown to match the current chosen option
$("#sort-selector").change(function() {
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
});

// listen for image field change in product management form
$("#new-image").change(function() {
    var file = $("#new-image")[0].files[0];
    $("#filename").text(`Image will be set to: ${file.name}`);
});

// for the dynamic array for track listing on add a product page
window.addEventListener("load", function() {
    function a(a) {
        a.querySelectorAll(".remove").forEach(a=>{
            a.addEventListener("click", ()=>{
                a.parentNode.remove();
            }
            );
        }
        );
    }
    function b(b) {
        const d = b.querySelector(".array-item"), e = d.cloneNode(!0), f = d.parentElement;
        d.getAttribute("data-isNone") && (d.remove(),
        e.removeAttribute("data-isNone"),
        e.removeAttribute("style")),
        a(b),
        b.querySelector(".add-array-item").addEventListener("click", ()=>{
            c++;
            const b = e.cloneNode(!0),
            d = b.querySelector("input").getAttribute("id").split("_"),
            g = d.slice(0, -1).join("_") + "_" + (c - 1 + "");
            b.querySelector("input").setAttribute("id", g),
            b.querySelector("input").value = "",
            a(b),
            f.appendChild(b);
        }
        );
    }
    let c = 1;
    $(".dynamic-array-widget").not(".empty-form .dynamic-array-widget").each((a,c)=>b(c)),
    $(document).on("formset:added", function(a, c) {
        c[0].querySelectorAll(".dynamic-array-widget").forEach(a=>b(a));
    });
});

// from Bootstrap, for disabling form submissions if there are invalid fields
(function() {
    "use strict";
    window.addEventListener("load", function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName("needs-validation");
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener("submit", function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add("was-validated");
        }, false);
      });
    }, false);
  })();
