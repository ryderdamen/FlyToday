<?php

/** 
	FlyToday API
	Description: Handles all incoming requests from DialogFlow, returns response from AVWX METAR API with witty comments
	Author: Ryder Damen | ryderdamen.com
*/


// Lifecycle --------------------------------------------------------------------------------------------------------------

// Retrieve POST body from the input stream
$json = file_get_contents('php://input');

// If we don't have anything, it's not a _POST, so just die silently
if ($json == '') {
	header('Location: https://ryderdamen.com/projects/fly-today/');
	die;
}



// Otherwise, let's decode this and grab some variables
$action = json_decode($json, true);
$airportCode = $action['result']['parameters']['airport']['ICAO'];
$airportFullName = $action['result']['parameters']['airport']['name'];
$airportCity = $action['result']['parameters']['airport']['city'];


// Now, let's call the AVWX API and get the METAR data
$metarJson = getMetar($airportCode);

// Send a JSON header so Google knows what to expect
header("Content-type:application/json");

// If we don't hear from the AVWX API, let's throw an error message for the user
if ($metarJson == '') {
	echo buildErrorResponse();
	die;
}

// Otherwise, let's send the weather so the pilots can get flying
echo buildResponse($metarJson, $airportCode, $airportFullName, $airportCity);


// Functions --------------------------------------------------------------------------------------------------------------

// Returns a general error message to dialogflow if something went wrong
function buildErrorResponse() {
	
	$default = "Hmm, I'm having a bit of trouble right now. It's probably best to look it up the old fashioned way. Sorry!";
	
	return json_encode(array(
		"speech" => $default,
		"displayText" => $default,
	));
}

// Returns the weather info to the user
function buildResponse($metarJson, $airportCode, $airportFullName, $airportCity) {
		
	// If the name of the airport contains the name of the city, just use the name of the airport
	if ( strpos( strtolower($airportFullName), strtolower($airportCity)) !== false ) {
		$response_airportName = $airportFullName;
	}
	else {
		$response_airportName = $airportFullName . ", " . $airportCity; 
	}
	
	// Say something based on whether it's VFR/IFR
	switch ($metarJson['Flight-Rules']) {
		case "LIFR":
			$response_full = "It's Looking like low IFR right now at " . $response_airportName;
			break;
		case "SVFR":
			$response_full = "It's Looking like special VFR right now at " . $response_airportName . ". Your call.";
			break;
		case "MVFR": 
			$response_full = "It's Looking like marginal VFR right now at " . $response_airportName . ". Your call.";
			break;
		case "VFR":
			$response_full = "Good news, it's VFR at " . $response_airportName . ". Let's go flying!";
			break;
		default:
			$response_full = "It's Looking like " . $metarJson['Flight-Rules'] . " right now at " . $response_airportName . ". Your call.";
	}
	
	return json_encode(array(
		"speech" => $response_full,
		"displayText" => $response_full,
	));
	
}

// Gets the flight rules from the JSON	
function getFlightRules($metarJson) {
	return $metarJson['Flight-Rules'];
}

// Gets the METAR from the API
function getMetar($code) {
	$baseUrl = 'https://avwx.rest/api/metar/';
	return json_decode(file_get_contents($baseUrl . $code), true);
}
	
