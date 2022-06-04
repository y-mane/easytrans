$(function() {
	$('.edit_user').click(function(e){
		var user_id = $(this).data('id');
		var url = '/manage-users/' + user_id + '/manage/';

		$.ajax({
			type: 'GET',
			url: url,
			dataType: 'json',
			success: function(data) {
				$('#user_id').val(data.id);
				$('#first_name').val(data.first_name);
				$('#last_name').val(data.last_name);
				$('#email').val(data.email);
				$('#id_proof').val(data.id_proof);
				$('#location').val(data.location);
				$('#work_phone').val(data.work_phone);
				$('#home_phone').val(data.home_phone);

				$(".group option").filter(function() {
					return $(this).val() == data.group; 
				}).prop('selected', true);

				$(".branch option").filter(function() {
					return $(this).val() == data.branch; 
				}).prop('selected', true);

			},error: function(e) {
			}
		});

	});

	$(".permissions").change(function(){
		var selected_options = $(this).val();
		$("#permissions").val(selected_options);
	});

	$('.assign_uperms').click(function(e){
		var user_id = $(this).data('id');
		var user_grp = $(this).data('grp');
		var user_name = $(this).data('uname');
		var url = '/manage-users-perms/' + user_id + '/manage/';

		$.ajax({
			type: 'GET',
			url: url,
			dataType: 'json',
			success: function(data) {
				$(".perms_modal_title").empty();
				$("#perms_details").empty();
				$('#puser_id').val(user_id);
				$(".perms_modal_title").append("Permissions: " + user_name + " [ " + user_grp + " ]");
				for (var i=0, len=data.length;i<len; i++) {
					$('#perms_details').append("- " + data[i] + "\n");
				}
			}
		});

	});

	$('.gperms').change(function(e){
		$(".permissions").empty();
		var selected_options = $(this).val();
		var url = '/api/v1/groups-perms/' + selected_options + '-group/';

		$.ajax({
			type: 'GET',
			url: url,
			dataType: 'json',
			success: function(data) {
				for (var i=0, len=data.length;i<len; i++) {
					var row = `<option value="${data[i][0]}">${data[i][1]}</option>`;
					$('.permissions').append(row);
				}
				$('.permissions').multiselect('rebuild');
			},
			error:function(e){
				console.log(e);
			}
		});
	});

	$('#user-modal').on("hidden.bs.modal", function(e){
		// $('#user_id').removeAttr('name')
		$('#user_id').val('');
		$('#first_name').val('');
		$('#last_name').val('');
		$('#id_proof').val('');
		$('#email').val('');
		$('#location').val('');
		$('#work_phone').val('');
		$('#home_phone').val('');
	});

	$('.dismiss_transit').click(function(e){
		// $('#user_id').removeAttr('name')
		$('#user_id').val('');
		$('#first_name').val('');
		$('#last_name').val('');
		$('#email').val('');
		$('#id_proof').val('');
		$('#location').val('');
		$('#work_phone').val('');
		$('#home_phone').val('');
	});

	//$('#user_form').submit(function(e){
		//e.preventDefault();
	//});
});
