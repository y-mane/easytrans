!function ($) {
    "use strict";

    var SweetAlert = function () {
    };

    //examples
    SweetAlert.prototype.init = function () {

        $('.delete_timeslot').click(function () {
			var timeslot_id = $(this).data('id');
			console.log("[+] Data-id: " + timeslot_id);
			var url = '/api/v1/timeslots/' + timeslot_id + '/';
			console.log("[+] Url: " + url);
			var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
			console.log("[+] csrf_token: " + csrf_token);

            swal({
                title: "Etes vous sur(e) ?",
                text: "Ce Créneau sera supprimé définitivement !",
                type: "warning",
                showCancelButton: true,
                cancelButtonClass: 'btn-default btn-md waves-effect',
                confirmButtonClass: 'btn-danger btn-md waves-effect waves-light',
                confirmButtonText: 'Supprimer',
                cancelButtonText: 'Annuler'
            }, function (isConfirm) {
                if (isConfirm) {
					console.log("[!] Confirm function launched. user confirmed delete");
					$.ajax({
						type: 'DELETE',
						url: url,
						headers:{"X-CSRFToken": csrf_token},
        				dataType: 'json',
						success: function(data) {
							// Reolading page
							window.location.reload(true);
						},error: function(e) {
							console.log("[%] Error: ");
							console.log(e);
						}
					});
                } else {
					console.log("[!] Deletion aborted!");
                }
            });
        });

    },
        //init
        $.SweetAlert = new SweetAlert, $.SweetAlert.Constructor = SweetAlert
}(window.jQuery),

//initializing
    function ($) {
        "use strict";
        $.SweetAlert.init()
    }(window.jQuery);
