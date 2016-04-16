(function() {
var elems = document.getElementsByTagName("div"),
   i;
for (i in elems) {
   if (elems[i].className == "wrapped") {
      var innerDiv = elems[i].getElementsByTagName("div");
      if (innerDiv[0].getElementsByTagName("a")[0].href.indexOf("/rajonchik37") > 0) {
         innerDiv[1].innerHTML = "***********************";
      }
   }
}
})();
