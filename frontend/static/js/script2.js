$(document).ready(function(){
  $("#advancedSearch").hide() ;

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

}) ;
