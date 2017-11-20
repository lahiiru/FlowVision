<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Debug Console</title>

    <link rel="stylesheet" href="bootstrap/css/bootstrap-theme.css">
    <link rel="stylesheet" href="bootstrap/css/bootstrap.css">
    <link rel="stylesheet" href="style.css"/>
    <script type="text/javascript" src="jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="bootstrap/js/bootstrap.js"></script>
</head>
<body>
<?php
// Saving...
$path = "../";

if(array_key_exists("_config", $_REQUEST)){
    unset($_REQUEST["_config"]);
    $json_str = json_encode($_REQUEST);
    file_put_contents("config.json", $json_str);
    $json_obj = json_decode($json_str);
    echo "<script type='application/javascript'>alert('Congiguration saved.');</script>";
}

if(array_key_exists("_conf", $_REQUEST)){
    unset($_REQUEST["_config"]);
    $json_str = json_encode($_REQUEST);
    file_put_contents("config.json", $json_str);
    echo "<script type='application/javascript'>alert('Congiguration saved.');</script>";
}
// Loading...
$cfg_path = "../";
$file_path = "C:/wamp/";
$config_str = file_get_contents("config.json");
$config_obj = json_decode($config_str);

var_dump($_FILES);
if( @$_FILES['file']['name'] != "" )
{
    echo $_FILES['file']['type'];
    $destFile = $file_path.$_FILES['file']['name'];
    move_uploaded_file( $_FILES['file']['tmp_name'], $destFile );
}

function get_server_cpu_usage(){

    $load = sys_getloadavg();
    print_r($load);
    return $load[0];

}
?>
<div class="container">
    <div class="row">
        <div class="col-lg-offset-2 col-md-2 col-sm-2 col-lg-8 col-md-8 col-sm-8 col-xs-12 bhoechie-tab-container">
            <div class="col-lg-2 col-md-2 col-sm-2 col-xs-3 bhoechie-tab-menu">
                <div class="list-group">
                    <a href="#" class="list-group-item active text-center">
                        <h4 class="glyphicon glyphicon-plane"></h4><br/>Status
                    </a>
                    <a href="#" class="list-group-item text-center">
                        <h4 class="glyphicon glyphicon-road"></h4><br/>Configuration
                    </a>
                    <a href="#" class="list-group-item text-center">
                        <h4 class="glyphicon glyphicon-home"></h4><br/>Update
                    </a>
                    <a href="#" class="list-group-item text-center">
                        <h4 class="glyphicon glyphicon-cutlery"></h4><br/>Logs
                    </a>
                    <a href="#" class="list-group-item text-center">
                        <h4 class="glyphicon glyphicon-credit-card"></h4><br/>Credit Card
                    </a>
                </div>
            </div>
            <div class="col-lg-9 col-md-9 col-sm-9 col-xs-9 bhoechie-tab">
                <!-- status section -->
                <div class="bhoechie-tab-content active">
                    <h4><strong><?php echo htmlspecialchars($config_obj->id); ?></strong></h4>
                    <table class="table table-bordered">
                        <thead>
                        <tr>
                            <th>Programs</th>
                            <th>Status</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>Main program</td>
                            <td>running</td>
                        </tr>
                        <tr>
                            <td>Communicator</td>
                            <td>running</td>
                        </tr>
                        <tr>
                            <td>Height measurement</td>
                            <td>running</td>
                        </tr>
                        </tbody>
                    </table>
                    <h6 class="text-right">Latest updated at: 17:56,2017/11/20</h6>
                    <!--<h6><Last updated at: 17:56,2017/11/20</h6>-->
                    <table class="table table-bordered">
                        <thead>
                        <tr>
                            <th colspan="2" class="text-center">Latest Measurements</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>Surface velocity (m/s)</td>
                            <td>13.42</td>
                        </tr>
                        <tr>
                            <td>Flow level (m)</td>
                            <td>0.21</td>
                        </tr>
                        <tr>
                            <td>Discharge (m3/s)</td>
                            <td>3.21</td>
                        </tr>
                        </tbody>
                    </table>
                    <h6 class="text-right">Latest updated at: 18:46,2017/11/20</h6>

                    <table class="table table-bordered">
                        <thead>
                        <tr>
                            <th colspan="2" class="text-center">System Info</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>CPU</td>
                            <td>100%</td>
                        </tr>
                        <tr>
                            <td>Memory(GB)</td>
                            <td>65%</td>
                        </tr>
                        <tr>
                            <td>Discharge (m3/s)</td>
                            <td>10%</td>
                        </tr>
                        </tbody>
                    </table>
                    <div class="text-right">
                        <button type="button" class="btn btn-info">Reset</button>
                        <button type="button" class="btn btn-warning">Restart</button>
                    </div>


                </div>
                <!-- configuration section -->
                <div class="bhoechie-tab-content">
                    <h4 class="text-left">Drainage Parameters</h4>

                    <form class="form-horizontal" method="get">
                        <input type="hidden" class="form-control" name="_config" placeholder="">
                        <div class="form-group">
                            <label class="control-label col-sm-4" for="email"><h5>Shape</h5></label>
                            <div class="radio">
                                <label><input type="radio" name="round">Round</label>
                            </div>
                            <div class="radio">
                                <label><input type="radio" name="rect">Rectangular</label>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="control-label col-sm-4" for="email"><h5>Diameter/ Width</h5></label>
                            <div class="col-sm-8">
                                <input type="text" value="<?php echo htmlspecialchars($config_obj->diameter); ?>" class="form-control" name="diameter" placeholder="diameter or width">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="control-label col-sm-4" for="pwd"><h5>Depth</h5></label>
                            <div class="col-sm-8">
                                <input type="text" value="<?php echo htmlspecialchars($config_obj->depth); ?>" class="form-control" name="depth" placeholder="depth">
                            </div>
                        </div>

                        <div class="h-divider"></div>
                        <h4 class="text-left">Location Details</h4>

                        <div class="form-group">
                            <label class="control-label col-sm-4" for="email"><h5>Meter Id</h5></label>
                            <div class="col-sm-8">
                                <input type="text" value="<?php echo htmlspecialchars($config_obj->id); ?>" class="form-control" name="id" placeholder="Meter id">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="control-label col-sm-4" for="pwd"><h5>Address</h5></label>
                            <div class="col-sm-8">
                                <input type="text" value="<?php echo htmlspecialchars($config_obj->address); ?>" class="form-control" name="address" placeholder="Installed location">
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="text-center">
                                <button type="submit" class="btn btn-primary">Update parameters</button>
                            </div>
                        </div>
                    </form>
                </div>

                <div class="bhoechie-tab-content">
                    <center>
                        <form action="upload.php" method="post" enctype="multipart/form-data">
                            Select image to upload:
                            <input type="file" name="fileToUpload" id="fileToUpload">
                            <input type="submit" value="Upload Image" name="submit">
                        </form>
                    </center>

                </div>

                <div class="bhoechie-tab-content">
                    ss
                </div>
                <div class="bhoechie-tab-content">
                    sss
                </div>
            </div>
        </div>
    </div>
</div>

<script type="application/javascript">
    $(document).ready(function () {
        $("div.bhoechie-tab-menu>div.list-group>a").click(function (e) {
            e.preventDefault();
            $(this).siblings('a.active').removeClass("active");
            $(this).addClass("active");
            var index = $(this).index();
            $("div.bhoechie-tab>div.bhoechie-tab-content").removeClass("active");
            $("div.bhoechie-tab>div.bhoechie-tab-content").eq(index).addClass("active");
        });
    });
</script>
</body>
</html>