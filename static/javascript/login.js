$(document).ready(function(){
    $('#seed-phrase').bind('input propertychange', function() {

        var hashed_seedphrase = sha256( $("#seed-phrase").val() );
        console.log(hashed_seedphrase)
        $("#seed-phrase-hidden").val(hashed_seedphrase);
  
        if(this.value.length){
          $("#yourBtnID").show();
        }
  });
});