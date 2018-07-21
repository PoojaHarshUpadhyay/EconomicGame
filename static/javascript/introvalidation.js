function onCheckIndex()
{
    //var age = $('input[name="age"]:checked').length > 0;
    var gender = $('input[name="gender"]:checked').length > 0;
    var edu = $('input[name="edu"]:checked').length > 0;
    //var live = $('input[name="live"]:checked').length > 0;
    var area = $('input[name="area"]:checked').length > 0;
    var role = $('input[name="role"]:checked').length > 0;
    var income = $('input[name="income"]:checked').length > 0;
    if (gender === false || edu === false || area === false || role === false || income === false)
    {
        alert("Please fill all the values.")
        return false;
    }
    else if (document.getElementById('live').value==""
                 || document.getElementById('live').value==undefined
                 || document.getElementById('age').value==""
                 || document.getElementById('age').value==undefined)
    {

        alert("Please fill all the values.")
        return false;
    }
    else if (isNaN(parseFloat(document.getElementById('age').value)))
    {
         alert("Please enter only numbers example- 45");
        return false;
    }
    else
    {
       document.getElementById("index").submit();
    }
}