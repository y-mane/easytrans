$(function() {
	// ------ Toast Actions -----------------------------------------------------------------------
    var toast = function(type, message) {
        toastr.options = {
            "closeButton": true,
            "debug": false,
            "newestOnTop": true,
            "progressBar": false,
            "positionClass": "toast-top-right",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "2500",
            "hideDuration": "2500",
            "timeOut": "8000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        };
        // tt = (type == 1) ? "success" : "error" ;
		var tt;
		if (type == 1){
			tt = "success";
		}else if (type == 2){
			tt = "error";
		}else if (type == 3){
			tt = "info";
		}else if (type == 4){
			tt = "warning";
		}else{
			console.log("[+] got type for toastr to be displayed: "+type)
		}
        toastr[tt](message);
    };

    if ($('.infos_type').text() == "1") {
        $('.showsuccesstoast').click(toast(1, $('.infos').text()));
	}else if ($('.infos_type').text() == "2") {
        $('.showerrortoast').click(toast(2, $('.infos').text()));
    }else if ($('.infos_type').text() == "3") {
        $('.showinfostoast').click(toast(3, $('.infos').text()));
    }else if ($('.infos_type').text() == "4") {
        $('.showwarningtoast').click(toast(4, $('.infos').text()));
    }



});

