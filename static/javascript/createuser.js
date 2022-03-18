$(document).ready(function(){
    $('#is-patient').click(function(){
        if($(this).prop("checked") == true){
            $("#patient-data").removeClass("hidden");
        }
        else if($(this).prop("checked") == false){
            $("#patient-data").addClass("hidden");
        }
    });

    $('#is-dentist').click(function(){
        if($(this).prop("checked") == true){
            $("#employee-data").removeClass("hidden");
            $("#dentist-data").removeClass("hidden");
        }
        else if($(this).prop("checked") == false){
            if ( ($("#is-admin").prop("checked") == false) && ($("#is-manager").prop("checked") == false)) {
                $("#employee-data").addClass("hidden");
            }
            $("#dentist-data").addClass("hidden");
        }
    });

    $('#is-admin').click(function(){
        if($(this).prop("checked") == true){
            $("#employee-data").removeClass("hidden");
        }
        else if($(this).prop("checked") == false){
            if ( ($("#is-dentist").prop("checked") == false) && ($("#is-manager").prop("checked") == false)) {
                $("#employee-data").addClass("hidden");
            }
        }
    });

    $('#is-manager').click(function(){
        if($(this).prop("checked") == true){
            $("#employee-data").removeClass("hidden");
        }
        else if($(this).prop("checked") == false){
            if ( ($("#is-admin").prop("checked") == false) && ($("#is-dentist").prop("checked") == false)) {
                $("#employee-data").addClass("hidden");
            }
        }
    });
});