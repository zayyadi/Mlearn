function onClickedEstimateBmi() {
    console.log("Estimate price button clicked");
    // var gender = document.getElementById("gender");
    // var weight = document.getElementById("weight");
    // var height = document.getElementById("height");
    var Bmi = document.getElementById("predictedBmi");
  
    var url = "predict_bmi";
  
    $.post(url, {
        gender: $('#gender').val(),
        weight: $('#weight').val(),
        height: $('#height').val()
    },function(data, status) {
        console.log(data.bmi);
        Bmi.innerHTML = "<h2>" + data.bmi.toString() + " Bmi </h2>";
        console.log(status);
    });
}
  
