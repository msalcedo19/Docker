$(document).ready(function(){

	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');

	});

	$('#sidebarCollapse_1').on('click', function () {
		$('#sidebar').toggleClass('active');
		
		var active = $('#sidebar').hasClass('active'); 
		if(active){
			$('#collapse-icon').removeClass('fas fa-angle-double-left');
			$('#collapse-icon').addClass('fas fa-angle-double-right');
			$("#collapse-icon").css("color", "white");

		}
		else{
			$('#collapse-icon').removeClass('fas fa-angle-double-right');
			$('#collapse-icon').addClass('fas fa-angle-double-left');
			$("#collapse-icon").css("color", "white");
		}

	});

	$.ajax({
		url: '/getItems',
		dataType: "json",
		type: 'GET',
		success: function(response){
			$.each(response, function(i, v){
				
				$('#items').append(
					'<div item class="col-lg-4 col-md-4 col-xs-12">'+
						'<div class="card card-beautify">' +
							'<img src="static/img/magic_box.jpg" class="card-img-top" alt="bad guy thumbnail">'+
							'<div class="card-body">'+
								'<h5 class="d-inline card-title">'+ v[1]+'</h5>'+
								'<p class="card-text">Id Item: '+ v[0] + '<br/> costo: '+ v[2]+ '</p>'+
								'<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#modal_compra" onclick="detailModal('
								+ v[0] + ')">Comprar</button>'+
							'</div>'+
						'</div>'+
					'</div>'
				);
			});
		},
		error: function(error){
			console.log(error);
		}
	});
});

function detailModal(id){
	$("#modal_compra_confirmBtn").attr('onclick', 'pagar('+ id+')');
}
async function  pagar(id){
	data = { items:{[id]:1}}
	res = await fetch("/complete_purchase", {method: 'POST', 
	body: JSON.stringify(data), // data can be `string` or {object}!
	headers:{
	  'Content-Type': 'application/json'
	}});

	if(res.status !== 200){
		console.log(res)

		$('#formAlerts').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">'+
									'<h4 class="alert-heading"><i class="fa fa-hand-paper"></i> Error </h4>'+
									'<p>'+ res.Message +'</p>'+
									'<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
									'<span aria-hidden="true">&times;</span>'+
									'</button>'+
								'</div>');
	}else{
		window.location.replace("/profile");
	}
}




