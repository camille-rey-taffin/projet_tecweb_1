$(document).ready(function(){
  $("#advancedSearch").hide() ;
  $("#Modification").hide() ;

  $("#boutonRecherche").click(function(){
    if ($("#boutonRecherche").html() == "Recherche avancée"){
        $("#boutonRecherche").html("Recherche simple");
        $("#advancedSearch").show() ;
    }
    else {
      $("#boutonRecherche").html("Recherche avancée");
      $("#advancedSearch").hide() ;
    }
});
  $("#boutonModify").click(function(){
    if ($("#boutonModify").attr("state") == "off"){
      $("#boutonModify").attr("state","on");
      $("#Modification").show() ;
  }
  else {
    $("#boutonModify").attr("state","off");
    $("#Modification").hide() ;
  }
});

$('.dropdown-sub .dropdown-list-sub a').on('touchstart', function(e) {
  e.preventDefault();
  window.location.href = $(this).attr('href');
})
}) ;

function deleteElement() {
  if (confirm("Etes-vous sûr(e) de vouloir supprimer l'élément ?")) {
    var curr_path = window.location.pathname;
    $.ajax({
      url: curr_path,
      method: 'DELETE',
      success : function(){
        $("#mainSection").empty();
        $( "#mainSection" ).append(
          "<div class='container'><div class='alert alert-success' role='alert'>L'élément <b>"
          + curr_path.substring(curr_path.lastIndexOf('/') + 1) +
          "</b> a bien été supprimé.</div><p class='lead' style='text-align:center'>Retourner à la page des <a href='/data/search'>données<a/></p></div>" );
        }
      })
    }
  };
