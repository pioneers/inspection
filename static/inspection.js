function allowDrop(ev) {
  ev.preventDefault();
  console.log("allowDrop");
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
  console.log("drag");

}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
  console.log("drop");

}

