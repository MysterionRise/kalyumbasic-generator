function removeMayonnaiseFromVK() {
  var elems = document.getElementsByTagName("div"),
    i;
  for (i in elems) {
    if (elems[i].className == "wrapped") {
      var innerDiv = elems[i].getElementsByTagName("div");
      if (innerDiv[0].getElementsByTagName("a")[0].href.indexOf("/rajonchik37") > 0 || innerDiv[0].getElementsByTagName("a")[0].href.indexOf("/anotherID") > 0) {
        innerDiv[1].innerHTML = Array(innerDiv[1].innerHTML.length + 1).join("*");
      }
    }
  }
}

function removeMayonnaiseFromSports() {

}

removeMayonnaiseFromVK();
removeMayonnaiseFromSports();
setInterval(removeMayonnaiseFromVK, 1000);
setInterval(removeMayonnaiseFromSports, 1000);
