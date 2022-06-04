$(function() {
	$('.update_branch').click(function(e){
		var branch_id = $(this).data('id');
		var url = '/manage-branches/' + branch_id + '/';

		$.ajax({
			type: 'GET',
			url: url,
			dataType: 'json',
			success: function(data) {
				$('#branch_id').val(data.id)
				$('#name').val(data.name)
				$('#phone').val(data.phone)
				$('#email').val(data.email)
				$('#address').val(data.address)
			},error: function(e) {
			}
		});

	});

	$('#branch-modal').on("hidden.bs.modal", function(e){
		$('#branch_id').val('')
		$('#name').val('')
		$('#phone').val('')
		$('#email').val('')
		$('#address').val('')
	});

	$('.dismiss_branch').click(function(e){
		$('#branch_id').val('')
		$('#name').val('')
		$('#phone').val('')
		$('#email').val('')
		$('#address').val('')
	});

    
});
