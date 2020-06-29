<!DOCTYPE html>
<html>
<head>
<title>Best Players</title>
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


    
let myRequest=new Request("./best_players.json");
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
    player+="<th>Player</th>";
    player+="<th>Team</th>";
    player+="<th>Puan</th>";
    player+="</tr>";
    for (var i = 0; i < data["2019/2020"].length; i++) { 
        player+="<tr>";
        player+="<td>"+data["2019/2020"][i].Oyuncu+"</td>";
        player+="<td>"+data["2019/2020"][i].Takım+"</td>";
        player+="<td>"+data["2019/2020"][i].player_importance+"</td>";
        player+="</tr>";
        
    }
    player+="</table>";
    
    document.getElementById("result").innerHTML=player;
});
 

function season_stats(s){
    
    var season=s.value;
    
    let myRequest=new Request("./best_players.json");
    
    fetch(myRequest)
    .then(function(resp){
        return resp.json();
    })
    .then(function(data){
        var player="<table>";
        player+="<tr>";
        player+="<th>Player</th>";
        player+="<th>Team</th>";
        player+="<th>Puan</th>";
        player+="</tr>";
        for (var i = 0; i < data[season].length; i++) { 
            player+="<tr>";
            player+="<td>"+data[season][i].Oyuncu+"</td>";
            player+="<td>"+data[season][i].Takım+"</td>";
            player+="<td>"+data[season][i].player_importance+"</td>";
            player+="</tr>";
            
        }
        player+="</table>";
        document.getElementById("result").innerHTML=player;
    });
}        


</script>

<script>

    $( document ).ready(function() {
        $("li:nth-child(4)").addClass("active");
    });

</script>

</body>
</html>