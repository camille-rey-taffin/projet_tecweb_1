$(document).ready(function(){
  $("#advancedSearch").hide() ;

  $("#boutonRecherche").click(function(){
    if ($("#boutonRecherche").attr("state") == "off"){
        $("#advancedSearch").show() ;
        $("#boutonRecherche").attr("state","on");
    }
    else {
      $("#boutonRecherche").attr("state","off");
      $("#advancedSearch").hide() ;
    }
});

}) ;
