<html>
<head> 
	<title> GPUA: Login</title>
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
		background-image: url("figs/{{img2}}");
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

	<form method="post" action="/gpapi/login">
	<h2 align= "center";>Login Form</h2>
		<div class="imgcontainer">
			<img src="figs/{{img1}}" alt="entry" class="avatar">
		</div>

		<div class="container">
			<label><b>Username:</b></label>
			<input type="text" placeholder="Enter Username" name="uname" >
			<span class="error">{{unameErr}}</span>

			<button type="submit">Login</button>
		</div>

		<div class="container" style="background-color:#dfdfdf" >
			<button type="button" onclick="location.href='/gpapi/register';" class="registerbtn">Register</button> 
			<button type="button" onclick="location.href='/gpapi/recover_psw';" class="registerbtn separate">Recover Password </button> 
		</div>
	</form>
</body>
</html>