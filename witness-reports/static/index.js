var toggleSubmit = function() {
    var isDisabled = document.getElementById("inputTitle").value.length == 0 || document.getElementById("inputNumber").value.length == 0
    
    var submitBtn = document.querySelector("input[type=submit]");
    
    if (isDisabled) {
      submitBtn.setAttribute("disabled", "disabled");
    } else {
      submitBtn.removeAttribute("disabled");
    }
  };
  
document.querySelector("form").addEventListener("input", toggleSubmit, false);

