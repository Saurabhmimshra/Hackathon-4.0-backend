<?php

require 'connect.inc.php';


phpinfo(); 


mysqli_set_charset( $con, 'utf8'); 
//for response
	// analysis fuction 

	function create_csv($con){

		//fetching data from db

		$query = "SELECT `monument_id`, `feedback_msg`, `transit_via`, `arrival`, `departure`, `visits`, `rating` FROM `trip` LEFT JOIN `monuments` ON `trip`.`monument_id` = `monuments`.`id`";

		// open the file "demosaved.csv" for writing
		$file = fopen('demosaved.csv', 'w');
		 
		// save the column headers
		fputcsv($file, array('monument_id', 'feedback_msg', 'transit_via', 'arrival', 'departure', 'visits', 'rating'));
		
		$data = mysqli_query($con, $query); 
		

		// Sample data. This can be fetched from mysql too


		 
		// save each row of the data
		foreach ($data as $row)
		{
			
		fputcsv($file, $row);
		}
		 
		// Close the file
		fclose($file);
	}

?>