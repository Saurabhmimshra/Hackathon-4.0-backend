<?php

require 'connect.inc.php';

mysqli_set_charset( $con, 'utf8'); 
//for response


	if(isset ($_POST['registration'])){
		$response = new \stdClass();
		if(isset($_POST['email']) && isset($_POST['password']) && isset ($_POST['name']) && isset ($_POST['age']) && isset ($_POST['gender']) && isset($_FILES['photo'])){
			$email = $_POST['email'];
			$name = $_POST['name'];
			$age = $_POST['age'];
			$gender = $_POST['gender'];
			$password = $_POST['password'];

			$file=$_FILES['photo'];
			$file_name=$file['name'];
			$file_tmp_loc=$file['tmp_name'];
			$file_error=$file['error'];
			$file_size=$file['size'];
			$file_type = $file['type'];
			$file_ext=explode('.',$file_name);
			$file_ext=strtolower(end($file_ext));
			$allow_type_array=array('image/jpeg');
			$allow_ext_array=array('png','jpg','jpeg');


			if(in_array($file_type, $allow_type_array)){
				if(in_array($file_ext, $allow_ext_array)){
					if ($file_error === 0) {
						if ($file_size <= 10857600) {
							
							date_default_timezone_set('Asia/Kolkata');
							$time=date('Y-m-d H:i:s',time());
							$ar=explode('.',$file_name);

							$file_new_name = uniqid().".".$file_ext;
							
							$query = "INSERT INTO `users`( `email`, `password` ,`name`, `age`, `gender`, `photo`) VALUES ('" . $email . "', '". $password ."' ,'". $name ."','". $age ."','". $gender ."', '" . $file_new_name . "')";
							// define('SITE_ROOT', realpath(dirname(__FILE__)));
							if (move_uploaded_file( $file_tmp_loc , 'images/profile/'.$file_new_name )){
								if(mysqli_query($con, $query)){
									$query = "SELECT MAX(`id`) FROM `users`";
									if ($result = mysqli_query($con, $query)) {
										$response->msg = mysqli_fetch_row($result)[0];
										$query = "INSERT INTO `location`(`user_id`) VALUES ('". $response->msg ."')";
										mysqli_query($con, $query);

										header('Content-Type: application/json');
										print json_encode($response,JSON_UNESCAPED_SLASHES);
									}
								}
							}
						}
					}
				}
			}
			
		}

		
	}


	// monuments : data retrieval

	if(isset($_POST['monuments_detail'])){
			$query = "SELECT `monuments`.`id`, `name`, `latitude`, `longitude`, `description`, `photo`, `rating`, `visits`, `fact1`, `fact2`, `fact3`, `fact4`, `fact5`, `fact6`, `fact7`, `fact8`, `fact9`, `fact10` FROM `monuments` LEFT JOIN `monument_facts` ON `monuments`.`id` = `monument_facts`.`monument_id`";
			$result = mysqli_query($con, $query);
			$data = array();
			foreach ($result as $row) {
				$data[] = $row;
			}
		header('Content-Type: application/json');
		print json_encode($data ,JSON_UNESCAPED_SLASHES);		
	}



	// // feedback form


// user_id, msg, monument name, transit_via, rating, 

if(isset($_POST['feedback'])){
	if(isset($_POST['user_id']) && isset($_POST['feedback_msg']) && isset($_POST['monument_name']) && isset($_POST['transit_via']) && isset($_POST['rating'])){

		$user_id = $_POST['user_id'];
		$feedback_msg = $_POST['feedback_msg'];
		$monument_name = $_POST['monument_name'];
		$transit_via = $_POST['transit_via'];
		$rating = $_POST['rating'];

		// fetch monument_id

		$query = "SELECT `id` FROM `monuments` WHERE '".$monument_name."' = `name`";
		$result = mysqli_query($con, $query);
		$monument_id = mysqli_fetch_row($result)[0];

		// insert into trip

		$query = "INSERT INTO `trip`(`user_id`, `monument_id`, `feedback_msg`, `transit_via`) VALUES ('". $user_id ."','". $monument_id ."','". $feedback_msg ."','". $transit_via ."')";
		$result = mysqli_query($con, $query);

		// insert into monument table

		$query = "SELECT `rating` from `monuments` where `id` = '". $monument_id ."'";
		$result = mysqli_query($con, $query);
		echo mysqli_error($con);
		$fetched_rating = mysqli_fetch_row($result)[0];
		$query = "SELECT COUNT(*) FROM `trip` WHERE `monument_id` = '". $monument_id ."'";
		$result = mysqli_query($con, $query);
		$count = mysqli_fetch_row($result)[0] ;
		$final = ($fetched_rating + $rating) / $count;
		$query = "UPDATE `monuments` SET `rating`= '". $final ."' WHERE `id` = '". $monument_id ."'";
		if(mysqli_query($con, $query)){
			$response = new \stdClass();
			$response->msg = True;
			header('Content-Type: application/json');
			print json_encode($response ,JSON_UNESCAPED_SLASHES);		
		}


	}
}



// for location

	if (isset($_POST['location'])) {
		if (isset($_POST['user_id']) && isset($_POST['lat']) && isset($_POST['long']) && isset($_POST['epoc'])) {
			$user_id = $_POST['user_id'];
			$lat = $_POST['lat'];
			$long = $_POST['long'];
			$epoc = $_POST['epoc'];

			// fetch monument_id

			$query = "SELECT `id` FROM `monuments` WHERE `latitude` = '". $lat ."' AND `longitude` = '". $long ."'";
			$result = mysqli_query($con, $query);
			$monument_id = mysqli_fetch_row($result)[0];


			date_default_timezone_set('Asia/Kolkata');
			$time1=date('Y-m-d H:i:s', $epoc);
			$time2 = date('Y-m-d H:i:s', $epoc + 7200);

			$query = "UPDATE `location` SET `monument_id`='". $monument_id ."',`arrival`= '". $time1."',`departure`= '". $time2 ."' WHERE `user_id`='". $user_id ."'";
			if(mysqli_query($con, $query)){
				$response = new \stdClass();
				$response->msg = True;
				header('Content-Type: application/json');
				print json_encode($response ,JSON_UNESCAPED_SLASHES);		
			}
		}
	}


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
