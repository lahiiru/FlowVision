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
$proc_mon_path = "/var/www/html/FlowVision/status/kill";

if(isset($_REQUEST["reset"])){

	file_put_contents($proc_mon_path, "");

    echo "<script type='application/javascript'>alert('Success. Processes will be up within 1 minute.');</script>";
}

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

function get_proc($name){
	$proc_mon_path = "/var/www/html/FlowVision/status/";
	$proc_mon_str = file_get_contents($proc_mon_path."proc_mon.json");
	$proc_mon_obj = json_decode($proc_mon_str, TRUE);

	if ($proc_mon_obj[$name]!=NULL){
		if($proc_mon_obj[$name]!="0"){
			return "Running.";
		}
	}
	return "Stopped.";
}
function get_m($param){
	$m_path = "/var/www/html/FlowVision/status/";
	$m_str = file_get_contents($m_path."measures.json");
	$m_obj = json_decode($m_str, TRUE);

	if ($m_obj[$name]!=NULL){
		return $m_obj[$name];
	}
	return "N/A";
}

function get_logs(){
	$log_file_path = "/var/www/html/FlowVision/iteration_3/src/device.log";
	exec("tail -n 30 $log_file_path | tac", $output);
	$output = implode("<br>", $output);
	return $output;
}

// Loading...
$cfg_path = "../";
$file_path = "/var/www/html/FlowVision/updates/";
$config_str = file_get_contents("config.json");
$config_obj = json_decode($config_str);

if( @$_FILES['file']['name'] != "" )
{
    if ($_FILES['file']['type'] == "application/x-zip-compressed"){

	}
    $destFile = $file_path.$_FILES['file']['name'];
    move_uploaded_file( $_FILES['file']['tmp_name'], $destFile );
}

function get_server_cpu_usage(){
    $load = sys_getloadavg();
    return $load[0];
}

function get_server_memory_usage(){

    $free = shell_exec('free');
    $free = (string)trim($free);
    $free_arr = explode("\n", $free);
    $mem = explode(" ", $free_arr[1]);
    $mem = array_filter($mem);
    $mem = array_merge($mem);
    $memory_usage = ($mem[2]/$mem[1])*100;

    return  round($memory_usage, 2);
}

function get_up_time(){
	$str   = @file_get_contents('/proc/uptime');
	$num   = floatval($str);
	$secs  = fmod($num, 60); $num = (int)($num / 60);
	$mins  = $num % 60;      $num = (int)($num / 60);
	$hours = $num % 24;      $num = (int)($num / 24);
	$days  = $num;
	return $days."d ".$hours."h ".$mins."m";
}

if (file_exists($proc_mon_path)){
	$kill = True;
}

?>
<div class="container">
    <div class="row">
        <div class="col-lg-offset-2 col-md-2 col-sm-2 col-lg-8 col-md-8 col-sm-8 col-xs-12 bhoechie-tab-container">
			<?php if($kill): ?>
			<div class="alert alert-warning" role="alert">
				ATTENTION: Programs restart is pending!
			</div>
			<?php endif; ?>
            <div class="col-lg-2 col-md-2 col-sm-2 col-xs-3 bhoechie-tab-menu">
                <div class="list-group">
                    <a href="#" class="list-group-item active text-center">
                        <h4 class="glyphicon glyphicon-signal"></h4><br/>Status
                    </a>
                    <a href="#" class="list-group-item text-center">
                        <h4 class="glyphicon glyphicon-cog"></h4><br/>Configuration
                    </a>
                    <a href="#" class="list-group-item text-center">
                        <h4 class="glyphicon glyphicon-refresh"></h4><br/>Update
                    </a>
                    <a href="#" class="list-group-item text-center">
                        <h4 class="glyphicon glyphicon-flag"></h4><br/>Logs
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
                            <td><?php echo get_proc("device.py"); ?></td>
                        </tr>
                        <tr>
                            <td>Communicator</td>
                            <td><?php echo get_proc("processor_1.py"); ?></td>
                        </tr>
                        <tr>
                            <td>Height measurement</td>
                            <td><?php echo get_proc("processor_2.py"); ?></td>
                        </tr>
                        </tbody>
                    </table>
                    <h6 class="text-right">Latest updated at: <?php echo htmlspecialchars(date("H:i:sa Y/m/d", $proc_mon_obj["timestmp"])); ?></h6>
                    <div class="text-right">
						<form>
                        <input type="submit" value="restart programs" name="reset" class="btn btn-large btn-warning">
						</form>
                    </div>
					<br>
                    <table class="table table-bordered">
                        <thead>
                        <tr>
                            <th colspan="2" class="text-center">Last Measurements</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>Surface velocity (m/s)</td>
                            <td><?php echo get_m('velocity'); ?></td>
                        </tr>
                        <tr>
                            <td>Flow level (m)</td>
                            <td><?php echo get_m('level'); ?></td>
                        </tr>
                        <tr>
                            <td>Discharge (m3/s)</td>
                            <td><?php echo get_m('discharge'); ?></td>
                        </tr>
                        </tbody>
                    </table>
                    <h6 class="text-right">Latest updated at:  <?php echo htmlspecialchars(date("H:i:sa Y/m/d", get_m('timestmp'))); ?></h6>

                    <table class="table table-bordered">
                        <thead>
                        <tr>
                            <th colspan="2" class="text-center">System Info</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>CPU utilization</td>
                            <td><?php echo get_server_cpu_usage(); ?>%</td>
                        </tr>
                        <tr>
                            <td>Memory usage</td>
                            <td><?php echo get_server_memory_usage(); ?>%</td>
                        </tr>
                        <tr>
                            <td>Uptime</td>
                            <td><?php echo get_up_time(); ?></td>
                        </tr>
						<tr>
                            <td>IP Address</td>
                            <td><?php echo $_SERVER['SERVER_ADDR']; ?></td>
                        </tr>
                        </tbody>
                    </table>
					<h6 class="text-right">Latest updated at: <?php echo date("H:i:sa Y/m/d"); ?></h6>


                </div>
                <!-- configuration section -->
                <div class="bhoechie-tab-content">
                    <h4 class="text-left">Drainage Parameters</h4>

                    <form class="form-horizontal" method="get">
                        <input type="hidden" class="form-control" name="_config" placeholder="">
                        <div class="form-group">
                            <label class="control-label col-sm-4" for="email"><h5>Shape</h5></label>
                            <div class="radio">
                                <label><input type="radio" name="round" value="1">Round</label>
                            </div>
                            <div class="radio">
                                <label><input type="radio" name="rect" disabled>Rectangular</label>
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
                        <form method="post" enctype="multipart/form-data">
                            Select update package to upload:
                            <input type="file" name="file" id="file">
                            <input type="submit" value="Upload" name="submit">
                        </form>
                    </center>

                </div>

                <div class="bhoechie-tab-content">
				<pre>
<?php
	echo get_logs();
?>
				</pre>
                </div>
                <div class="bhoechie-tab-content">

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