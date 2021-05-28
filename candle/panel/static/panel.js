'use strict';

//Collapsible search menu:
var buttons = document.getElementsByClassName("panel_cast_button");
let i;
for (i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", function() {
    this.classList.toggle("active");  // add or remove class
    var content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "%";
    }
  });
}
