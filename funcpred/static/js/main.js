$(document).ready( function () {
    $('#data_table').DataTable({
	    "order": [[ 3, "asc" ]],
	    paging: false,
	    "language": {
		"search": "refine search:"
	   }
    });
} );
