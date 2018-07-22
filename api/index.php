<?php

/** 
	FlyToday API
	Description: Handles all incoming requests from DialogFlow, returns response from AVWX METAR API with witty comments
	Author: Ryder Damen | ryderdamen.com
*/

include('webhook.php');
$wh = new Webhook('fly-today');

// Get Parameters
$airport = $wh->get_parameter('airport');
$airportCode = $airport['ICAO'];
$airportFullName = $airport['name'];
$airportCity = $airport['city'];

// Call the AVWX API and build a response for the user
$metarJson = getMetar($airportCode);

if ($metarJson == '') { // If there was an error retrieving the JSON
	$errorText = "Sorry, something wen't wrong retrieving the weather data.";
	$wh->build_simpleResponse($errorText, $errorText);
	$wh->respond();
	die;
}

// If the name of the airport contains the name of the city, just use the name of the airport
if ( strpos( strtolower($airportFullName), strtolower($airportCity)) !== false ) {
	$response_airportName = $airportFullName;
} else {
	$response_airportName = $airportFullName . ", " . $airportCity; 
}

// Say something based on whether it's VFR/IFR
switch ($metarJson['Flight-Rules']) {
	case "LIFR":
		$response_text = "It's looking like low IFR right now at " . $response_airportName . " 🙁";
		$response_speech = "It's looking like low IFR.";
		break;
	case "SVFR":
		$response_text = "It's looking like special VFR right now at " . $response_airportName . ". Your call.";
		$response_speech = "It's looking like special VFR.";
		break;
	case "MVFR": 
		$response_text = "It's looking like marginal VFR right now at " . $response_airportName . ". Your call.";
		$response_speech = "It's looking like marginal VFR.";
		break;
	case "VFR":
		$response_text = "Good news, it's VFR at " . $response_airportName . ". Let's go flying! 🛩";
		$response_speech = "Good news, it's VFR.";
		break;
	default:
		$response_text = "It's Looking like " . $metarJson['Flight-Rules'] . " right now at " . $response_airportName . ". Your call.";
		$response_speech = "It's Looking like " . $metarJson['Flight-Rules'] . " right now at " . $response_airportName . ". Your call.";
}

$wh->build_simpleResponse($response_speech, $response_text);
$wh->respond();


// Gets the METAR from the API
function getMetar($code) {
	$baseUrl = 'https://avwx.rest/api/metar/';
	return json_decode(file_get_contents($baseUrl . $code), true);
}
	
