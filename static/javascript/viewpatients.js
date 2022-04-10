$(document).ready(function(){

    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    
       
 // Show Input element
 $('.edit').click(function(){
    $('.txtedit').hide();
    $(this).next('.txtedit').show().focus();
    $(this).hide();
   });

    $(".txtedit").focusout(function(){
    
        // Get edit id, field name and value
        var id = this.id;
        var split_id = id.split("_");
        var field_name = split_id[0];
        var edit_id = split_id[1];
        var value = $(this).val();
          
        // Hide Input element
        $(this).hide();
        
        // Hide and Change Text of the container with input elmeent
        $(this).prev('.edit').show();
        $(this).prev('.edit').text(value);
        
        $.ajax({
         url: '/update',
         type: 'post',
         data: { field:field_name, value:value, id:edit_id },
         success:function(response){
            if(response == 1){ 
               console.log('Save successfully'); 
            }else{ 
               console.log("Not saved.");  
            }
         }
        });
         
       });

    // Delete row on delete button click
    $(document).on("click", ".delete", function(){
        $(this).parents("tr").remove();
        $(".add-new").removeAttr("disabled");
        var id = $(this).attr("id");
        var string = id;
        
         $.post("/delete", { string: string}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        }); 
    });

    // update row 
    $(document).on("click", ".update", function(){
        var id = $(this).attr("id");
        var string = id;
        var txtssn = $("#txtssn").val();
        var txtaddress = $("#txtaddress").val();
        var txtphone = $("#txtphone").val();
       $.post("/update", { string: string,txtssn: txtssn, txtaddress: txtaddress, txtphone: txtphone}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        }); 
         
         
    }); 
    
    // Edit row
    $(document).on("click", ".edit", function(){  
        $(this).parents("tr").find("td:not(:last-child)").each(function(i){
           // if (i=='0'){
             //   var idname = 'txtssn';
            if (i=='1'){
                var idname = 'txtaddress';
            }else if (i=='2'){
                var idname = 'txthousenumber';
            } else if (i=='3') {
              var idname ='txtstreetname';
            } else if (i=='4'){
              var idname ='txtstreetnumber';
            } else if (i=='5'){
                var idname = 'txtcity'
            } else if (i=='6'){
                var idname = 'txtprovince';
            } else if (i=='7') {
                var idname = 'txtfirstname'
            } else if (i=='8') {
                var idname = 'txtmiddlename';
            } else if (i=='9') {
                var idname = 'txtlastname';
            } else if (i=='10') {
                var idname = 'txtgender'
            } else if (i=='11'){
                var idname = 'txtemailaddress'
            }else if (i=='12'){
                var idname = 'txtdateofbirth'
            } else if (i =='13'){
                var idname = 'txtphonenumber'
            } else if (i =='14'){
                var idname = 'txtage'
            } else if (i == '15'){
                var idname = 'txtpassword'
            }else{} 
            $(this).html('<input type="text" name="updaterec" id="' + idname + '" class="form-control" value="' + $(this).text() + '">');
        });  
        $(this).parents("tr").find(".edit").toggle();
        $(".add-new").attr("disabled", "disabled");
        $(this).parents("tr").addClass("update"); 
    });
});
