function activate_data_table(){
    var order_col=$('#data_table').data("order_col") -1; 
    if(!order_col == undefined ){
	    order_col=3;
    }
    $('#data_table').DataTable({
	    "order": [[ order_col, "asc" ]],
	    paging: false,
	    "language": {
		"search": "refine search:"
	   }
    });


}
$(document).ready( function () {
    activate_data_table();
} );
