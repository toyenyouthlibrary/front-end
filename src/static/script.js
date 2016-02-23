
function neste(url){
    var inputs = document.getElementsByTagName("input");
    var empty_fields = false;
    if(inputs.length != 0){
        for(var x = 0; x < inputs.length; x++){
            if(inputs[x].value == ""){
                empty_fields = true;
                inputs[x].className += " formInvalid";
                if(inputs[x].getAttribute("placeholder") == null){
                    document.getElementById("error").innerHTML = "Feil pinkode, pr&oslash;v igjen.";
                }
            }
        }
    }
    if(!empty_fields){
        //Gå til neste
        document.getElementsByTagName("form")[0].submit();
    }
}

window.onload = function(){
    if(typeof pin !== "undefined"){
        var inputs = document.getElementsByTagName("input");
        inputs[0].focus();
        for(var i = 0; i < inputs.length; i++){
            inputs[i].addEventListener("keyup", function(){
                if(this.value != "" && this.nextElementSibling != null){
                    this.nextElementSibling.focus();
                }
            });
        }
    }
};