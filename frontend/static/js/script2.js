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

}) ;
