<!DOCTYPE html>
<html>
<head>
<title>Preseason Predictions</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<!-- Popper JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
<!-- Latest compiled JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>

<link rel="stylesheet" href="tables.css">
</head>
<body>

<?php
    include("topbar.php");
?>

<div id="result"> </div>

<script type="text/javascript">


    
let myRequest=new Request("./before_season_prediction.json");
//fetch("./best_players.json")
fetch(myRequest)
.then(function(resp){
    return resp.json();
})
.then(function(data){
    //document.write("<h1>"+data["2019/2020"][0]["Oyuncu"]+"</h1>");
    //document.write(data["2019/2020"].length);
    var player="<table>";
    player+="<tr>";
    player+="<th>Takım</th>";
    player+="<th>Number of Matches</th>";
    player+="<th>Predicted Wins</th>";
    player+="<th>True Wins</th>";
    player+="<th>Pro Predicted Wins</th>";
    player+="</tr>";
    for (var i = 0; i < data["2019/2020"].length-1; i++) { 
        player+="<tr>";
        player+="<td>"+data["2019/2020"][i].Takım+"</td>";
        player+="<td>"+data["2019/2020"][i].n_matches+"</td>";
        player+="<td>"+Math.round(data["2019/2020"][i].adjusted_w)+"</td>";
        player+="<td>"+data["2019/2020"][i].true_w+"</td>";
        player+="<td>"+data["2019/2020"][i].pro_pred+"</td>";
        player+="</tr>";
        
    }
    player+="</table>";
    player+="<hr>";
    player+="RMSE: "
    player+=data["2019/2020"][data["2019/2020"].length-1].RMSE;
    player+="<br>";
    player+="RMSE Pro: "
    player+=data["2019/2020"][data["2019/2020"].length-1].RMSE_pro;
    document.getElementById("result").innerHTML=player;
});
 

function season_stats(s){
    
    var season=s.value;
    
    let myRequest=new Request("./before_season_prediction.json");
    
    fetch(myRequest)
    .then(function(resp){
        return resp.json();
    })
    .then(function(data){
        var player="<table>";
        player+="<tr>";
        player+="<th>Takım</th>";
        player+="<th>Number of Matches</th>";
        player+="<th>Predicted Wins</th>";
        player+="<th>True Wins</th>";
        if (season=="2019/2020")
            {player+="<th>Pro Predicted Wins</th>";}
        player+="</tr>";
        for (var i = 0; i < data[season].length-1; i++) { 
            player+="<tr>";
            player+="<td>"+data[season][i].Takım+"</td>";
            player+="<td>"+data[season][i].n_matches+"</td>";
            player+="<td>"+Math.round(data[season][i].adjusted_w)+"</td>";
            player+="<td>"+data[season][i].true_w+"</td>";
            if (season=="2019/2020")
                {player+="<td>"+data["2019/2020"][i].pro_pred+"</td>";}
            player+="</tr>";
            
        }
        player+="</table>";
        player+="<hr>";
        player+="RMSE: "
        player+=data[season][data[season].length-1].RMSE;
        player+="<br>";
        if (season=="2019/2020"){
            player+="RMSE Pro: "
            player+=data["2019/2020"][data["2019/2020"].length-1].RMSE_pro;
        }
        document.getElementById("result").innerHTML=player;
    });
}        

</script>

<script>

    $( document ).ready(function() {
        $("li:nth-child(2)").addClass("active");
    });

</script>

</body>
</html>