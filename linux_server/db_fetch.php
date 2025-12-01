<?php
$env = parse_ini_file(__DIR__ . "/../.env");

$servername = $env["SERVER_NAME"]; // server_ip
$username = $env["USERNAME"]; // no need -> katso discordin pinned-viesteistä
$password = $env["PASSWORD"]; // no need -> katso discordin pinned-viesteistä
$dbname = $env["DB_NAME"];
// $groupid = XX; // oma groupid

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
        }

$sql = "SELECT timestamp, sensorvalue_x, sensorvalue_y, sensorvalue_z, sensor_orientation FROM rawdata ORDER BY id"; // DESC LIMIT 20";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
   while($row = $result->fetch_assoc()) {
      echo "Time: " . $row["timestamp"] . " - Sensor X: " . $row["sensorvalue_x"] . " - Sensor Y: " . $row["sensorvalue_y"]. " - Sensor Z: " . $row["sensorvalue_z"]. " - Sensor Orientation: " . $row["sensor_orientation"] ."<br>" ;   }
} else {
	echo "No data found.";
}

$conn->close();
?>

