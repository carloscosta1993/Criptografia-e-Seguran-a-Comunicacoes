<html>
<head> 
	<title> GPUA: Challenge Failure </title>
</head>
<style>
	form {
		background-color: #ffffff;
		margin: auto;
		width: 30%;
		margin-top: 40px;
		border: 3px solid #73AD21;
		padding: 10px;
	}
	
	body {
		background-image: url("/gpapi/figs/{{img2}}");
	}

	h2{
		color: #91c27b;
		font-height: 900;
		font-size: 1.7em;

	}
	
	input[type=text]
	{
	    width: 100%;
	    padding: 12px 20px;
	    margin: 8px 0;
	    display: inline-block;
	    border: 1px solid #ccc;
	    box-sizing: border-box;
	}

	button {
	    background-color: #4CAF50;
	    color: white;
	    padding: 14px 20px;
	    margin: 8px 0;
	    border: none;
	    cursor: pointer;
	    width: 100%;
	}

	.registerbtn {
	    width: auto;
	    padding: 10px 18px;
	    background-color: #f44336;
	}

	.imgcontainer {
	    text-align: center;
	    margin: 24px 0 12px 0;
	}

	img.avatar {
	    width: 40%;
	    border-radius: 0%;
	}

	.container {
	    padding: 16px;
	}

	.separate{margin-left: 10px;}
	
	.error {color: #FF0000;}

</style>
<body>

	<form method="post">
		<h2 align= "center">Success!</h2>
		<div class="imgcontainer">
			<img src="/gpapi/figs/{{img6}}" alt="entry" class="avatar">
		</div>

		<div class="container">
			<label style="text-align: center;"><b>You have successfully completed the challenge. You are now logged in. </b></label>
		</div>

		<div class="container" style="background-color:#dfdfdf" >
			<button type="button" text-align="center" onclick="location.href='/gpapi/login';" class="registerbtn">Home</button> 
		</div>

	</form>
</body>
</html>