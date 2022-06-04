!function ($) {
    "use strict";

    var SweetAlert = function () {
    };

    //examples
    SweetAlert.prototype.init = function () {

        //Basic
        $('#sa-basic').click(function () {
            swal("Here's a message!");
        });

        //A title with a text under
        $('#sa-title').click(function () {
            swal("Here's a message!", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lorem erat, tincidunt vitae ipsum et, pellentesque maximus enim. Mauris eleifend ex semper, lobortis purus sed, pharetra felis")
        });

        //Success Message
        $('#sa-success').click(function () {
            swal("Good job!", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lorem erat, tincidunt vitae ipsum et, pellentesque maximus enim. Mauris eleifend ex semper, lobortis purus sed, pharetra felis", "success")
        });

        //Warning Message
        $('#sa-warning').click(function () {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonClass: 'btn-warning',
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            }, function () {
                swal("Deleted!", "Your imaginary file has been deleted.", "success");
            });
        });

        //Parameter
        $('#sa-params').click(function () {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                cancelButtonText: "No, cancel plx!",
                closeOnConfirm: false,
                closeOnCancel: false
            }, function (isConfirm) {
                if (isConfirm) {
                    swal("Deleted!", "Your imaginary file has been deleted.", "success");
                } else {
                    swal("Cancelled", "Your imaginary file is safe :)", "error");
                }
            });
        });

        //Custom Image
        $('#sa-image').click(function () {
            swal({
                title: "Sweet!",
                text: "Here's a custom image.",
                imageUrl: "../plugins/bootstrap-sweetalert/thumbs-up.jpg"
            });
        });

        //Auto Close Timer
        $('#sa-close').click(function () {
            swal({
                title: "Auto close alert!",
                text: "I will close in 2 seconds.",
                timer: 2000,
                showConfirmButton: false
            });
        });

        //Primary
        $('#primary-alert').click(function () {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "info",
                showCancelButton: true,
                cancelButtonClass: 'btn-default btn-md waves-effect',
                confirmButtonClass: 'btn-primary btn-md waves-effect waves-light',
                confirmButtonText: 'Primary!'
            });
        });

        //Info
        $('#info-alert').click(function () {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "info",
                showCancelButton: true,
                cancelButtonClass: 'btn-default btn-md waves-effect',
                confirmButtonClass: 'btn-info btn-md waves-effect waves-light',
                confirmButtonText: 'Info!'
            });
        });

        //Success
        $('#success-alert').click(function () {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "success",
                showCancelButton: true,
                cancelButtonClass: 'btn-default btn-md waves-effect',
                confirmButtonClass: 'btn-success btn-md waves-effect waves-light',
                confirmButtonText: 'Success!'
            });
        });

        //Warning
        $('#warning-alert').click(function () {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                cancelButtonClass: 'btn-default btn-md waves-effect',
                confirmButtonClass: 'btn-warning btn-md waves-effect waves-light',
                confirmButtonText: 'Warning!'
            });
        });




		// Gestion de la Suppression d'un evenement ---------------------------
        //Danger
        $('.delete_event').click(function () {
			var event_id = $(this).data('id');
			console.log("[+] Data-id: " + event_id);
			var url = '/api/v1/events/' + event_id + '/';
			console.log("[+] Url: " + url);
			// We get an csrf_token for making query. because of login state we
			// have to provide a csrf_token for queries
			var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
			console.log("[+] csrf_token: " + csrf_token);

            swal({
                title: "Etes vous sur(e) ?",
                text: "Vous ne pourrez plus le récupérer. La cagnotte associée sera désactivée.",
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
							// console.log("[%] Data: " + data);
							// console.log(data);
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

		// Gestion de la Suppression d'un evenement ---------------------------
        //Danger
        $('.delete_pool').click(function () {
			var pool_id = $(this).data('id');
			console.log("[+] Data-id: " + pool_id);
			var url = '/api/v1/pools/' + pool_id + '/';
			console.log("[+] Url: " + url);
			// We get an csrf_token for making query. because of login state we
			// have to provide a csrf_token for queries
			var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
			console.log("[+] csrf_token: " + csrf_token);

            swal({
                title: "Etes vous sûr(e) ?",
                text: "Vous ne pourrez plus le récupérer. La cagnotte sera supprimée.",
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
							// console.log("[%] Data: " + data);
							// console.log(data);
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


		// Gestion de la Suppression d'un evenement ---------------------------
        //Danger
        $('.disable_pool').click(function () {
			var pool_id = $(this).data('id');
			console.log("[+] Data-id: " + pool_id);
			var url = '/api/v1/pools/' + pool_id + '/disable/';
			console.log("[+] Url: " + url);
			// We get an csrf_token for making query. because of login state we
			// have to provide a csrf_token for queries
			// var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
			// console.log("[+] csrf_token: " + csrf_token);

            swal({
                title: "Etes vous sûr(e) ?",
                text: "Personne ne pourra effectuer un dépôt. La Cagnotte sera désactivée.",
                type: "warning",
                showCancelButton: true,
                cancelButtonClass: 'btn-default btn-md waves-effect',
                confirmButtonClass: 'btn-danger btn-md waves-effect waves-light',
                confirmButtonText: 'Désactiver',
                cancelButtonText: 'Annuler'
            }, function (isConfirm) {
                if (isConfirm) {
					console.log("[!] Confirm function launched. user confirmed delete");
					$.ajax({
						type: 'GET',
						url: url,
						// headers:{"X-CSRFToken": csrf_token},
        				dataType: 'json',
						success: function(data) {
							// console.log("[%] Data: " + data);
							// console.log(data);
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

		// Gestion de la Suppression d'une cagnotte ---------------------------
        //Danger
        $('.delete_ticket').click(function () {
			var ticket_id = $(this).data('id');
			console.log("[+] Data-id: " + ticket_id);
			var url = '/api/v1/tickets/' + ticket_id + '/';
			console.log("[+] Url: " + url);
			// We get an csrf_token for making query. because of login state we
			// have to provide a csrf_token for queries
			var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
			console.log("[+] csrf_token: " + csrf_token);

            swal({
                title: "Etes vous sur(e) ?",
                text: "Vous ne pourrez plus avoir de réponse du support pour ce ticket ",
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
							// console.log("[%] Data: " + data);
							// console.log(data);
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
