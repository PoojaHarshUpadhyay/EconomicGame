
$('document').ready(function(){

   var counter = parseInt($("#hdnCtn").val());

   if (counter > 10)
   {
        $('#ctnSimulation1').removeAttr('disabled');
        $("#ctnConfirm").hide();
        $("#ctnAddRound").hide();
   }
   else
   {
        $('#ctnSimulation1').attr('disabled','disabled');
         if (counter === 1)
        {
            $("#ctnConfirm").show();
            $("#ctnAddRound").hide();
        }
        else
        {
            $("#ctnConfirm").hide();
            $("#ctnAddRound").show();
        }
   }
});

function myContinueSim1()
{
   var roundvalue = $("#round").text();
    console.log(roundvalue);
    if (roundvalue === "Round 1")
    {
        document.getElementById("continue_simulationPageOne").submit();
    }
    else if (roundvalue === "Round 2")
    {
        document.getElementById("continue_simulationPageTwo").submit();
    }
     else if (roundvalue === "Round 3")
    {
        document.getElementById("continue_simulationPageThree").submit();
    }
     else if (roundvalue === "Round 4")
    {
        document.getElementById("continue_simulationPageFour").submit();
    }
}

function myConfirmRound1() {
    var lastyear = '';
     var lastgrossIncome = '';
     var lastrepIncome = '';
     var counter = parseInt($("#hdnCtn").val());
     console.log(counter)
   $('#maintable tr').each(function() {
     lastyear = $(this).find("td[id='year']:last").text();
     lastgrossIncome = $(this).find("td[id='grossIncome']:last").text();
   });
   lastgrossIncome = lastgrossIncome.trim();
   lastyear = lastyear.trim();
   lastgrossIncome = parseFloat(lastgrossIncome);
   lastrepIncome =  $('table#maintable tr:last input[name=repIncomeFirst]').val();
   console.log(lastrepIncome);
   lastrepIncome = parseFloat(lastrepIncome);
   if (lastrepIncome === '' || lastgrossIncome === "" || lastgrossIncome === null)
   {
   alert("Please enter - Reported income");
    return false;
   }
   else if (isNaN(parseFloat(lastrepIncome)))
   {
   alert("Please enter only numbers - like 12345");
   return false;
   }
   else if (lastrepIncome < 0 || lastrepIncome > lastgrossIncome)
   {
   alert("Please enter only from 0 to Gross income");
   return false;
   }
   else
   {
    $('input[type="hidden"][name="year"]')
                  .val(lastyear);
   $('input[type="hidden"][name="grossIncome"]')
                  .val(lastgrossIncome);
   $('input[type="hidden"][name="repIncome"]')
                  .val(lastrepIncome);
    $("#ctnConfirm").hide();

    var roundvalue = $("#round").text();
    console.log(roundvalue);
    if (roundvalue === "Round 1")
    {
        document.getElementById("continue_simulationPageOne").submit();
    }
    else if (roundvalue === "Round 2")
    {
        document.getElementById("continue_simulationPageTwo").submit();
    }
     else if (roundvalue === "Round 3")
    {
        document.getElementById("continue_simulationPageThree").submit();
    }
     else if (roundvalue === "Round 4")
    {
        document.getElementById("continue_simulationPageFour").submit();
    }
   }

}


function ctnAddRound1() {
    var $tbody = $("#maintable tbody");
    var lastyear = parseInt($tbody.find("td[id='year']:last").text()) + 1;
    var lastgrossIncome = parseInt($tbody.find("td[id='grossIncome']:last").text()) + 100;
    var repIncome = getNum(parseInt($tbody.find("input[id='repIncomeFirst']").value));
    var incomeTax = getNum(parseInt($tbody.find("label[id='incomeTax']").val()));
    var grossIncomeLessTax = getNum(parseInt($tbody.find("label[id='grossIncomeLessTax']").val()));
    var audited = getNum(parseInt($tbody.find("label[id='audited']").val()));
    var rowFine = getNum(parseInt($tbody.find("label[id='rowFine']").val()));
    var grossIncomeLessTaxLessFine = getNum(parseInt($tbody.find("label[id='grossIncomeLessTaxLessFine']").val()));
    var markup = "<tr  class='rTableRow'><td class='rTableHead' id='year'>"+lastyear+"</td><td class='rTableHead' id='grossIncome'>" + lastgrossIncome + "</td><td class='rTableHead'><input type='input' name='repIncomeFirst'  id='repIncome'>"+repIncome+"</td><td class='rTableHead'>" + incomeTax + "</td><td class='rTableHead'>" + grossIncomeLessTax + "</td><td class='rTableHead'>" +  audited+ "</td><td class='rTableHead'>" + rowFine + "</td><td class='rTableHead'>" + grossIncomeLessTaxLessFine + "</td></tr>";
    $("table tbody").append(markup);
    $("#ctnConfirm").show();
    $("#ctnAddRound").hide();
}

function getNum(val) {
   if (isNaN(val)) {
     return "";
   }
   return val;
}