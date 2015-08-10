function l_in()
{
	var p0 = document.getElementById("password0").value;
	
	if(p0.length < 8)
	{
		alert("Password must be at least 8 characters long");
		return ;
	}
	
	var username = document.getElementById("email0").value;
	var temp_result;
		
	if (typeof(Storage) == "undefined")
	{	
        alert("Sorry, your browser does not support Web Storage...");
		return ;
	}
	   
    
	
	temp_result = serverstub.signIn(username, p0); 

    if(temp_result.success == false)
	{
		alert("Wrong user or password");
		return ;
	}
	
	alert("Successfully signed in!");
	localStorage.setItem("current_user", temp_result.data);
	alert(localStorage.getItem("current_user"));
	location.reload();
	
    
}


function s_up()
{
	var p1 = document.getElementById("password1").value;
	var p2 = document.getElementById("password2").value;
	
	if(p1.length < 8)
	{
		alert("Password must be at least 8 characters long");
		return ;
	}
	
	if(p1.localeCompare(p2) != 0)
	{
		alert("Password mismatch!");
		return ;
	}
	
	var gen;
	
	if(document.getElementById("gender1").checked)
		gen = "male"
	else
		gen = "female"
	
	var signup_data = {
		email : document.getElementById("email1").value,
        password : p1,
        firstname : document.getElementById("fname1").value,
        familyname : document.getElementById("lname1").value,
        gender : gen,
        city : document.getElementById("city1").value,
        country : document.getElementById("country1").value

	};
	
	alert(serverstub.signUp(signup_data).message);
	
}

function fun_welcomeview()
{
	if(localStorage.getItem("current_user") == 0)
        document.getElementById("main").innerHTML = document.getElementById("welcomeview").innerHTML; 
	else
		document.getElementById("main").innerHTML = document.getElementById("profileview").innerHTML; 
}

