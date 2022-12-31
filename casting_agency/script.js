$(document).ready(function () {
  $.get("http://127.0.0.1:5000/actor", function (actor) {
    console.log(actor);
    var list = "";
    var count = 0;
    for (var i = actor.length - 1; i >= 0; i--) {
      count++;
      list +=
        "<tr>" +
        "<td>" +
        count +
        "</td>" +
        "<td>" +
        actor[i].name +
        "</td>" +
        "<td>" +
        actor[i].gender +
        "</td>" +
        "<td>" +
        actor[i].age +
        "</td>" +
        "<td>" +
        actor[i].nationality +
        "</td>" +
        "<td>" +
        '<button type="button" class="btn btn-primary waves-effect waves-light" onclick="edit(' +
        actor[i].id +
        ')"><i class="mdi mdi-pen"></i></button> ' +
        '<button type="button" class="btn btn-danger waves-effect waves-light" onclick="remove(' +
        actor[i].id +
        ')"><i class="mdi mdi-close"></i></button></td>' +
        "</tr>";
    }
    $("#actorlist").html(list);

    $("#list").DataTable();
  });
});
