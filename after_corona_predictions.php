<!DOCTYPE html>
<html>
<head>
<title>After Corona Predictions</title>
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


    
let myRequest=new Request("./afterCorona_prediction.json");
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
    player+="<th>My Predictions</th>";
    player+="<th>Pro Predictions</th>";
    player+="</tr>";
    for (var i = 0; i < data.length-1; i++) { 
        player+="<tr>";
        player+="<td>"+data[i].Takım+"</td>";
        player+="<td>"+Math.round(data[i].adjusted_w)+"</td>";
        player+="<td>"+data[i].pro_pred+"</td>";
        player+="</tr>";
        
    }
    player+="</table>";
    player+="<hr>";
    player+="RMSE: "
    player+=data[data.length-1].RMSE;

    document.getElementById("result").innerHTML=player;
});
 

</script>
<script>

    $( document ).ready(function() {
        $("li:nth-child(1)").addClass("active");
    });

</script>
</body>
</html>