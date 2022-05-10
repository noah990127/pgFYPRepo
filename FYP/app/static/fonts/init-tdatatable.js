// ========================================================================= //
//   Table Example 1
// ========================================================================= //

// Start DataTable

let ex1 = jQuery('#example1').DataTable({});

// Delete Row Datatable

$('#example1 tbody').on('click', 'a.delet span', function() {
    ex1
        .row($(this).parents('tr'))
        .remove()
        .draw();
});


// ========================================================================= //
//   Table Example 2
// ========================================================================= //

// Hide colmun Datatable 

let ex2 = jQuery('#example2').DataTable({

    "columnDefs": [{
        "targets": [3],
        "visible": false
    }, {
        "targets": [5],
        "visible": false
    }, {
        "targets": [8],
        "visible": false
    }, {
        "targets": [9],
        "visible": false
    }, {
        "targets": [10],
        "visible": false
    }, {
        "targets": [11],
        "visible": false
    }, {
        "targets": [12],
        "visible": false
    }, ]


});

// Function show modal resultat patient

$('#example2 tbody').on('click', '.vue', function() {
    // getting target row data
    var data = ex2.row($(this).parents('tr')).data();
    $('.insertHere').html(
        // Adding and structuring the full data
        '<table class="table table-striped table-responsive-sm modalShowTable" width="100%"><tbody><tr><td>First Name<td><td>' + data[1] + '</td></tr><tr><td>Last name<td><td>' + data[2] + '</td></tr><tr><td>Email<td><td>' + data[3] + '</td></tr><tr><td>Mobile No.<td><td>' + data[4] + '</td></tr><tr><td>Birthday<td><td>' + data[5] + '</td></tr><tr><td>Marital status<td><td>' + data[6] + '</td></tr><tr><td>Sex<td><td>' + data[7] + '</td></tr> <tr><td>Blood Group<td><td>' + data[8] + '</td></tr> <tr><td>Patient Weight<td><td>' + data[9] + '</td></tr> <tr><td>Patient Height<td><td>' + data[10] + '</td></tr> <tr><td>Address<td><td>' + data[11] + '</td></tr> <tr><td>Patient History<td><td>' + data[12] + '</td></tr></tbody></table>'
    );
    // calling the bootstrap modal
    $('#myModal').modal('show');

});

// Delete Row Datatable

$('#example2 tbody').on('click', '.delet', function() {
    ex2
        .row($(this).parents('tr'))
        .remove()
        .draw();
});

// ========================================================================= //
//   Table Example 3
// ========================================================================= //

// Billing List Table

var ex3 = jQuery('#example3').DataTable({
    dom: 'lrtip',
    "ordering": false,
    "bPaginate": true,
    "bInfo": true,
    "bSort": false,
    "lengthChange": false,

});

// Delete Row Datatable

$('#example3 tbody').on('click', '.delet', function() {
    ex3
        .row($(this).parents('tr'))
        .remove()
        .draw();
});

// Filter by Date inside datatable

var ex3 = $("#example3").DataTable();

minDateFilter = "";
maxDateFilter = "";

$("#daterange").daterangepicker();
$("#daterange").on("apply.daterangepicker", function(ev, picker) {
    minDateFilter = Date.parse(picker.startDate);
    maxDateFilter = Date.parse(picker.endDate);

    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
        var date = Date.parse(data[1]);

        if (
            (isNaN(minDateFilter) && isNaN(maxDateFilter)) ||
            (isNaN(minDateFilter) && date <= maxDateFilter) ||
            (minDateFilter <= date && isNaN(maxDateFilter)) ||
            (minDateFilter <= date && date <= maxDateFilter)
        ) {
            return true;
        }
        return false;
    });
    ex3.draw();
});

// Select filter inside datatable

$('.table-filter-select').on('change', function() {
    ex3.search(this.value).draw();
});

// Form search inside table

$('#myInputTextField').keyup(function() {
    ex3.search($(this).val()).draw();
})