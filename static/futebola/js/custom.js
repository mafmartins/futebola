$( document ).ready(function() {
    for (var i = 0; i < 1000; i++){
        if ($("#nome-Equipa_B-"+i).length){
            var temp = $("#nome-Equipa_B-"+i).html();
            $("#nome-Equipa_B-"+i).html($("#golos-Equipa_B-"+i).html());
            $("#golos-Equipa_B-"+i).html(temp);
            $("#golos-Equipa_B-"+i).css("text-align", "right");
            $("#nome-Equipa_B-"+i).css("text-align", "center");
        }
    }
    
    $("#back").click(function(){
        window.history.back();
        console.log("TEste!");
    });
    
    
    
    $("#crit").click(function(){
        $("#crits").toggle(1000);
    });
});

