<!DOCTYPE html>
<html>
<head>

<title>Top Bar</title>
<link rel="stylesheet" href="topbar.css">
<!-- <script src="topbar.js"></script>  -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

</head>
<body>
<div class="topbar">

    <ul>
        <li><a href="after_corona_predictions.php">After Corona Predictions</a></li>
        <li><a href="preseason_predictions.php">Preseason Predictions</a></li>
        <li><a href="monthly_prediction.php">Monthly Predictions</a></li>
        <li><a href="best_players.php">Best Players</a></li>
        <li style="float:right">
            <div>
            <select class="form-control myselect" name="select_year" id="select_year" onchange="season_stats(this);">
                <option value="2019/2020" selected>2019/2020</option>
                <option value="2018/2019">2018/2019</option>
                <option value="2017/2018">2017/2018</option>
                <option value="016/2017">2016/2017</option>
                <option value="2015/2016">2015/2016</option>
                <option value="2014/2015">2014/2015</option>
                <option value="2013/2014">2013/2014</option>
            </select>
            </div>
        </li>
    </ul>

</div>
</body>
</html>

