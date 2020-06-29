<!DOCTYPE html>
<html>
<head>
<title>Monthly Predictions</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<!-- Popper JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
<!-- Latest compiled JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>

<link rel="stylesheet" href="tables.css">
<style>
    #select_div_month{
        position:absolute;
        top:20%;
        left:90% ;
    }
</style>

</head>
<body>

<?php
    include("topbar.php");
?>
<div class="container">
<div id="result"> </div>

<div id="select_div_month">
    <select name="choose_month" id="choose_month" class="form-control myselect" onchange="season_stats(this);" >
        <option value="4" selected>April</option>
        <option value="3">March</option>
        <option value="2">February</option>
        <option value="1">January</option>
        <option value="12">December</option>
    </select>
</div>
</div>

<script type="text/javascript">


    
let myRequest=new Request("./monthly_predictions.json");
//fetch("./best_players.json")
fetch(myRequest)
.then(function(resp){
    return resp.json();
})
.then(function(data){
    //document.write("<h1>"+data["2019/2020"][0]["Oyuncu"]+"</h1>");
    //document.write(data["2019/2020"].length);
    var m=document.getElementById("choose_month").value;
    //alert(m);
    var player="<table>";
    player+="<tr>";
    player+="<th>Takım</th>";
    player+="<th>Number of Matches Made</th>";
    player+="<th>Number of Matches Left</th>";
    player+="<th>Predicted Wins</th>";
    player+="<th>True Wins</th>";
    player+="</tr>";
    for (var i = 0; i < data["2019/2020"][m].length-1; i++) { 
        player+="<tr>";
        player+="<td>"+data["2019/2020"][m][i].Takım+"</td>";
        player+="<td>"+data["2019/2020"][m][i].n_matches_made+"</td>";
        player+="<td>"+data["2019/2020"][m][i].n_matches_left+"</td>";
        player+="<td>"+Math.round(data["2019/2020"][m][i].adjusted_w)+"</td>";
        player+="<td>"+data["2019/2020"][m][i].true_w+"</td>";
        player+="</tr>";
        
    }
    player+="</table>";
    player+="<hr>";
    player+="RMSE: "
    player+=data["2019/2020"][m][data["2019/2020"][m].length-1].RMSE;
    document.getElementById("result").innerHTML=player;
});
 

function season_stats(s){

    var season=document.getElementById("select_year").value;
    //alert(season);
    var m=document.getElementById("choose_month").value;
    let myRequest=new Request("./monthly_predictions.json");
    
    fetch(myRequest)
    .then(function(resp){
        return resp.json();
    })
    .then(function(data){
        var player="<table>";
        player+="<tr>";
        player+="<th>Takım</th>";
        player+="<th>Number of Matches Made</th>";
        player+="<th>Number of Matches Left</th>";
        player+="<th>Predicted Wins</th>";
        player+="<th>True Wins</th>";
        player+="</tr>";
        for (var i = 0; i < data[season][m].length-1; i++) { 
            player+="<tr>";
            player+="<td>"+data[season][m][i].Takım+"</td>";
            player+="<td>"+data[season][m][i].n_matches_made+"</td>";
            player+="<td>"+data[season][m][i].n_matches_left+"</td>";
            //player+="<td>"+data[season][m][i].adjusted_w+"</td>";
            player+="<td>"+Math.round(data[season][m][i].adjusted_w)+"</td>";
            player+="<td>"+data[season][m][i].true_w+"</td>";
            player+="</tr>";
            
        }
        player+="</table>";
        player+="<hr>";
        player+="RMSE: "
        player+=data[season][m][data[season][m].length-1].RMSE;
        document.getElementById("result").innerHTML=player;
    });
}        

document.getElementById("choose_month").addEventListener("onchange", season_stats);


</script>

<script>

    $( document ).ready(function() {
        $("li:nth-child(3)").addClass("active");
    });

</script>

</body>
</html>