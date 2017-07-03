<html>
<head> 
	<title> GPUA: Registration</title>
</head>
<style>


	input[type=text]
	{
	    width: 55%;
	    padding: 4px 20px;
	    margin: 2px;
	    display: inline-block;
	    border: 1px solid #ccc;
	    box-sizing: border-box;
	}
	
	input[type=email]
	{
	    width: 55%;
	    padding: 4px 20px;
	    margin: 2px;
	    display: inline-block;
	    border: 1px solid #ccc;
	    box-sizing: border-box;
	}
	
	body {
		background-image: url("/gpapi/figs/{{img2}}");
	}

	button {
	    background-color: #4CAF50;
	    vertical-align: bottom;
	    color: white;
	    padding: 14px 20px;
	    margin: 8px 0;
	    border: none;
	    cursor: pointer;
	    width: 80%;
	}

	.top {
		background-image: url("/gpapi/figs/{{img3}}");
		margin-top: -8px;
		margin-left: -8px;
		position:fixed;
		width:100%;
	}

	.bottom {
		margin-left: -8px;
		position:fixed;
		bottom: 0px;
		background-image: url("/gpapi/figs/{{img3}}");
		width:100%;
	}

	.container_top {
 	    padding: 16px;
	}
	
	.container {
 	    padding: 16px;
		width: 70%;
		margin: auto;
	}
	
	div.img {
	    margin: 5px;
	    border: 1px solid #ccc;
	    float: left;
	    width: 150px;
	}

	div.img:hover {
	    border: 1px solid #777;
	}

	div.img img {
	    width: 150px;
	    height: auto;
	}

	.pswbox{
		background:white;
	    float: left;
	    width: 100px;
	    height: 100px;
	    margin: 5px;
	    border: 1px dashed black;
	}

	.error {color: #FF0000;}

</style>

<body>

<div class="top">
	<center>
		<form method="post" action="/gpapi/register">
		<div class="container_top">
			<label style="color: #4CAF50;"><b>Username:&nbsp;	</b></label><input type="text" placeholder="Enter Username" name="uname">
			<span class="error">{{unameErr}}</span>
			<br></br>
			<label style="color: #4CAF50;"><b>Email:&nbsp;	</b></label><input type="email" placeholder="Enter Email" name="uemail">
			<span class="error">{{uemailErr}}</span>
		</div>
	</center>           
</div>

<div style="width: 100%; padding-top:7em; padding-bottom:12em;">
	<div class="container" style="background-color:#fafafa;">
		<center> <table cellspacing="8">	
			<% num_rows=get('num_rows');num_cols=get('num_cols');total=1 %>
			<% for i in range(1,num_rows+1): %>
				<tr>
				<% for j in range(1,num_cols+1): %>
					<% img = "%s%d.png" % (get('imgpsw'),total) %>
					<td>
					<div class='img'>
						<img src="/gpapi/figs/{{img}}" alt="entry" onclick="Click({{total}})" width=150px height=150px>
					</div>
					</td>
					<% total=total+1 %>
				<% end %>
				</tr>
				<tr>
				<% for j in range(num_cols): %>
					<td>
						<div style='text-align:center'>
							<% caption = "Img. " + str(total-num_cols+j) %>
							<b style='color: #4CAF50;'> {{caption}} </b>
						</div>
					</td>
				<% end %>
				</tr>
			<% end %>
		</table> </center>
	</div>
</div>

<div class="bottom">
	<center> <div class="container" style="float:left; width:75%;">

	<label><b style="color: #4CAF50;">Portfolio</b> <i> <small>- You must remember the images selected and their relative order </small> </i> </label>
		<center> <table cellspacing="8">
		<tr>
		<% for i in range(1,N+1): %>
			<td>
				<div class='pswbox'>
				<% imgID="MyImg_%d" % (i) %>
				<img id={{imgID}} scr="/gpapi/figs/{{img5}}" width=100px height=100px>
				</div>
			</td>
		<% end %>
		</tr>
	
		<tr>
		<% for i in range(1,N+1): %>
			<td>
			<div style='text-align:center'>
				<% selID="Select_%d" % (i) %>
				<% func3="SelectImg(this,%d)" % (i) %>
				<select name={{selID}} id={{selID}} onchange={{func3}}>
					<option selected hidden value='0'> Choose one </option>
				<% for j in range(1,M+1): %>
					<% val= "Img. %d" % (j) %>
					<option value={{j}}> {{val}} </option>
				<% end %>
				</select>
				<img src="/gpapi/figs/{{img4}}" onclick="Erase({{i}})" width=12px height=12px>
			</div>
			</td>
		<% end %>
		</tr>
		</center> </table>
	</div> </center>

	<div class="container" style="float:left; width:19%;">
	<br> </br> <br> </br>  
	<center> 
		<button type="submit" onclick="ConfirmMessage()" >Submit </button>
		<button type="button" style="background-color: #f44336;" onclick="location.href='/gpapi/login';">Home</button> 
	</center>
	</div> 
</div>

</form>

<script>

	function Click(id){
		Empty=0;
		for (i = 1; i <= {{N}}; i++) {
			var id1 = "Select_".concat(i);
			if(document.getElementById(id1).value==0){
				Empty=1;
				break;}}
		if(Empty){
			var MyImgS = "MyImg_".concat(i)
			document.getElementById(MyImgS).src="/gpapi/figs/{{imgpsw}}"+id+".png";
			document.getElementById(id1).value=id;}
	}
	
	function Erase(i){
		var id1 = "Select_".concat(i);
		var id2 = "MyImg_".concat(i);
		document.getElementById(id1).value=0;	
		document.getElementById(id2).src="/gpapi/figs/{{img5}}";
	}

	function SelectImg(elem,i){
		var id = "MyImg_"+i
		var MyImgS=document.getElementById(id);
		MyImgS.src="/gpapi/figs/psw/img_"+elem.value+".png";
	}

	function ConfirmMessage(){
		return confirm('\tPlease attent the password you selected below and \t\t\t\tconfirm your registration\t');
	}

</script>

</body>
</html>