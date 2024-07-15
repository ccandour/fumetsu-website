$(document).ready(function(){

	$(".bt_com_sh").click(function() {
		var th = $(".box_com").has(this)
		var t = $(".com_val", th).text().trim();
		var r = $(".pdk", th).val();
		var l = $(".ideph", th).val();
		$('#modalComRe input.textinput').attr("placeholder", t);
		$('#modalComRe input.pdk').val(r);
		if(typeof l !== "undefined"){
			$('#modalComRe input.ideph').val(l);
		}
	});

	$(".bt_com_del").click(function() {
		var th = $(".box_com").has(this)
		var r = $(".pdk", th).val();
		var l = $(".ideph", th).val();
		$('#modalComDel input.pdk').val(r);
		if(typeof l !== "undefined"){
			$('#modalComDel input.ideph').val(l);
		}
		console.log(l);
	});

	$(".tlm").click(function(){
	    var name = $(this).attr('value');
	    if ($("#"+name).is(":visible") == 0){
            $("#"+name).show();
        }
        else{
            $("#"+name).hide();
        }
      });

});