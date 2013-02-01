/*Prints a table of tftarget values. It is independentto the number of 
columns and rows returned
@params 
table - the table you want to append a row to.
object - the json object
row_num - to distinguish between a heading and data ....will think of a better way. If row_num == 0, it meas it is a heading otherwise data.
*/
function printTable (table, object, row_num) {
 //initialize the row
    var row = '<tr>';
    if(row_num == 0) { // table heading
        for (property in object) {
            row += '<td>' + property + '</td>';
        }
        table.append(row);
        var row = '<tr>';
    }
    for (property in object) {
        if (property == 'pmid') {
            row += '<td><a href="http://www.ncbi.nlm.nih.gov/pubmed/' + object[property] + '">' + object[property] + '</a></td>';
        } else {
            row += '<td>' + object[property] + '</td>';
        }
    }
    row += '</tr>'; //end the row, ready to append
    table.append(row);
}


function ajaxSearch () {
    $.post('/', $('#search_form').serialize(), function (data) {
    //clear the search result for ready for next search result
    $('#search_results').children().remove()
    //create a table here
    var table = $('<table></table>').addClass('table table-condensed table-striped table-hover');
        for (var i = 0; i < data.length; i++) {
            printTable(table, data[i], i);
        }
       $('#search_results').append(table);
    }, 'json');
}


$(document).ready(function () {
    console.log("We're loading jQuery, jQuery UI, and our own custom js!");
    $.ajaxSetup({traditional: true});

    $('#search_button').click(ajaxSearch);
    $('.input-text').keypress(function (e) {
        if (e.which == 13) {
            console.log('enter pressed');
            ajaxSearch();
        }
    });
    $('.input-select').change(ajaxSearch);
});
