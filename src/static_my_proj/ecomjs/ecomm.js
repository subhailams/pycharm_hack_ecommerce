$(document).ready(function () {

  //Contact Form

  var contactForm = $(".form-horizontal")
  var contactFormMethod = contactForm.attr("method")
  var contactFormEndpoint = contactForm.attr("action")
  var contactFormSubmitBtn = contactForm.find("[type='submit']")
  var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

  function displaySubmitting(submitBtn, defaultText, doSubmit) {
    if (doSubmit) {
      submitBtn.addClass("disabled")
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
    } else {
      submitBtn.removeClass("disabled")
      submitBtn.html(defaultText)
    }

  }


  contactForm.submit(function (event) {
    event.preventDefault()




    var contactFormData = contactForm.serialize()
    var thisForm = $(this)
    displaySubmitting(contactFormSubmitBtn, "", true)
    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function (data) {
        console.log("Contact Data:",data.message)
        contactForm[0].reset()
        // $.alert("success bro")
        $.alert({
          
          content: data.message,
          theme: "modern",
        })
        setTimeout(function () {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)
      },
      error: function (error) {
        console.log(error)
        console.log(error.responseJSON)
        var jsonData = error.responseJSON
        var msg = ""

        $(jsonData, function (key, value) {

          msg += key + ": " + value[0].message + "<br/>"
        })

        $.alert({
          // title: "Oops!",
          content: data.message,
          theme: "modern",
        })

        setTimeout(function () {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)

      }
    })
  })


  





  //Auto Search
  var searchForm = $(".search-form")
  var searchInput = searchForm.find("[name='q']") // input name='q'
  var typingTimer;
  var typingInterval = 500 // .5 seconds
  var searchBtn = searchForm.find("[type='submit']")
  searchInput.keyup(function (event) {
    // key released
    clearTimeout(typingTimer)

    typingTimer = setTimeout(perfomSearch, typingInterval)
  })

  searchInput.keydown(function (event) {
    // key pressed
    clearTimeout(typingTimer)
  })

  function displaySearching() {
    searchBtn.addClass("disabled")
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i>")
  }

  function perfomSearch() {
    displaySearching()
    var query = searchInput.val()
    setTimeout(function () {
      window.location.href = '/search/?q=' + query
    }, 600)

  }

  








  var productForm = $(".form-product-ajax") // #form-product-ajax

  productForm.submit(function (event) {
    event.preventDefault();
    console.log("Form is not sending")
    var thisForm = $(this)
    // var actionEndpoint = thisForm.attr("action");
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function (data) {
        console.log("success")
        var submitSpan = thisForm.find(".submit-span")
        if (data.added) {
          submitSpan.html("In cart <button type='submit' class='btn btn-link'>Remove?</button>")
        } else {
          submitSpan.html("<button type='submit'  class='btn btn-success'>Add to cart</button>")
        }
        var navbarCount = $(".navbar-cart-count")
        navbarCount.text(data.cartItemCount)
        var currentPath = window.location.href
        if (currentPath.indexOf("cart") != -1) {
          refreshCart()
        }
      },
      error: function (errorData) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern",
        })
      }

    })

  })
  function refreshCart() {
    console.log("in current cart")
    // var cartBody = $(".cart-header")
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    // cartBody.html("<h1>Changed</h1>")
    var shoppingCart = cartBody.find(".cart-items")
    var productRows = cartBody.find(".cart-header")
    var currentUrl = window.location.href
    var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

    var refreshCartUrl = 'cart/api/cart/'
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function (data) {
        console.log("success")
        console.log(data)

        // shoppingCart.html(" ")
        // shoppingCart.prepend("<h2>My Shopping Bag("+data.products.length+")")
        if (data.products.length > 0) {
          productRows.html(" ")
          $.each(data.products, function (index, value) {
            console.log(value)
            var newCartItemRemove = hiddenCartItemRemoveForm.clone()
            newCartItemRemove.css("display", "block")
            // newCartItemRemove.removeClass("hidden-class")
            newCartItemRemove.find(".cart-item-product-id").val(value.id)
            productRows.prepend("<div class=\"cart-header\"><div class=\"cart-sec\"><div class=\"cart-item cyc\"><img src=" + value.image + "/></div><div class=\"cart-item-info\"></h2><h4>" + value.name + "</h4></span><br/><h4><span>Model No:3578</span></h4><h4>Rs." + value.price + "</h4><h4><span>Qty: " + value.qty + "</span></h4>" + newCartItemRemove.html() + "</div><div class=\"clearfix\"></div><div class=\"delivery\"><p>Service Charges:: Rs.100.00</p><span>Delivered in 2-3 bussiness days</span><div class=\"clearfix\"></div></div></div></div>")

          })

          cartBody.find(".cart-subtotal").text(data.subtotal)
          cartBody.find(".final").text(data.total)
        }
        else {
          window.location.href = currentUrl
        }
      },
      error: function (errorData) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern",
        })
      }
    })


  }


  //password-validation
	var myInput = document.getElementById("input-pwd");
	var letter = document.getElementById("letter");
	var capital = document.getElementById("capital");
	var number = document.getElementById("number");
	var length = document.getElementById("length");
	
	// When the user clicks on the password field, show the message box
	myInput.onfocus = function() {
	  document.getElementById("message").style.display = "block";
	}
	
	// When the user clicks outside of the password field, hide the message box
	myInput.onblur = function() {
	  document.getElementById("message").style.display = "none";
	}
	
	// When the user starts to type something inside the password field
	myInput.onkeyup = function() {
	  // Validate lowercase letters
	  var lowerCaseLetters = /[a-z]/g;
	  if(myInput.value.match(lowerCaseLetters)) {  
		letter.classList.remove("invalid");
		letter.classList.add("valid");
	  } else {
		letter.classList.remove("valid");
		letter.classList.add("invalid");
	  }
	  
	  // Validate capital letters
	  var upperCaseLetters = /[A-Z]/g;
	  if(myInput.value.match(upperCaseLetters)) {  
		capital.classList.remove("invalid");
		capital.classList.add("valid");
	  } else {
		capital.classList.remove("valid");
		capital.classList.add("invalid");
	  }
	
	  // Validate numbers
	  var numbers = /[0-9]/g;
	  if(myInput.value.match(numbers)) {  
		number.classList.remove("invalid");
		number.classList.add("valid");
	  } else {
		number.classList.remove("valid");
		number.classList.add("invalid");
	  }
	  
	  // Validate length
	  if(myInput.value.length >= 8) {
		length.classList.remove("invalid");
		length.classList.add("valid");
	  } else {
		length.classList.remove("valid");
		length.classList.add("invalid");
	  }
	}
	var myInput = document.getElementById("input-pwd1");
	var letter = document.getElementById("letter");
	var capital = document.getElementById("capital");
	var number = document.getElementById("number");
	var length = document.getElementById("length");
	
	// When the user clicks on the password field, show the message box
	myInput.onfocus = function() {
	  document.getElementById("message").style.display = "block";
	}
	
	// When the user clicks outside of the password field, hide the message box
	myInput.onblur = function() {
	  document.getElementById("message").style.display = "none";
	}
	
	// When the user starts to type something inside the password field
	myInput.onkeyup = function() {
	  // Validate lowercase letters
	  var lowerCaseLetters = /[a-z]/g;
	  if(myInput.value.match(lowerCaseLetters)) {  
		letter.classList.remove("invalid");
		letter.classList.add("valid");
	  } else {
		letter.classList.remove("valid");
		letter.classList.add("invalid");
	  }
	  
	  // Validate capital letters
	  var upperCaseLetters = /[A-Z]/g;
	  if(myInput.value.match(upperCaseLetters)) {  
		capital.classList.remove("invalid");
		capital.classList.add("valid");
	  } else {
		capital.classList.remove("valid");
		capital.classList.add("invalid");
	  }
	
	  // Validate numbers
	  var numbers = /[0-9]/g;
	  if(myInput.value.match(numbers)) {  
		number.classList.remove("invalid");
		number.classList.add("valid");
	  } else {
		number.classList.remove("valid");
		number.classList.add("invalid");
	  }
	  
	  // Validate length
	  if(myInput.value.length >= 8) {
		length.classList.remove("invalid");
		length.classList.add("valid");
	  } else {
		length.classList.remove("valid");
		length.classList.add("invalid");
	  }
	}
});