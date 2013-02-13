/**
   This is a collection of JavaScript functions. 
   @author - Djenome Team - Tremayne Mushayahama, Joel Friedly, Grant Michalski, Edward Powell
   @primary author - Tremayne Mushayahama
   @date 2/7/2013
*/


/**
   This table orders the column of the table. The purpose of the multidimensional array is to 
   map from DB name to Human readable format
   eg. expt_type - Experimental Type
*/
var TABLE_HEADING = [["transcription_factor", "Transcription Factor"],
                     ["gene", "Gene"],
                     ["pmid", "PMID"],
                     ["species", "Experimental Species"],
                     ["expt_tissues", "Experimental Tissues"],
                     ["cell_line", "Cell Line"],
                     ["expt_type", "Experimental Type"]];


var INPUT_NAME = [["id_transcription_family", "Transcription Family"],
                  ["id_transcription_factor", "Transcription Factor"],
                  ["id_gene", "Gene"],
                  ["id_species", "Experiment Species"],
                  ["id_tissue_name", "Experiment Tissues"],
                  ["id_expt_type", "Experiment Type"]];


/**
   Prints the headings of the table from a json object. The result is appended to the table
   @param thead - the thead element of the table
   @param object - the json object
*/
function printTHead (thead) {
    var row = '<tr>';
    //for (property in object) {
    for(var i=0; i < TABLE_HEADING.length; i++) {
       row += '<th>' + TABLE_HEADING[i][1] + '</th>';
    }
    row += '</tr>'
    thead.append(row);
}


/**
   Prints the rest of the table from a json object. The result is appended to the table
   @param tbody - the tbody element of the table
   @param object - the json object
*/
function printTBody (tbody, object) {
    var row = '<tr>';
    for (var i=0; i < TABLE_HEADING.length; i++) {
        property = TABLE_HEADING[i][0];
        if (property == 'pmid') {
            row += '<td><a href="http://www.ncbi.nlm.nih.gov/pubmed/' + object[property] + '">' + object[property] + '</a></td>';
        } else {
            row += '<td>' + object[property] + '</td>';
        }
    }
    row += '</tr>'; //end the row, ready to append
    tbody.append(row);
}


//initSearchForm require that values are in pairs label and a bunch of ctrols.
function initSearchForm () {
    console.log('Beautifying your search form');
    var $searchForm = $('#tft-search-form').children();
    /*add the class control-label to all labels in the
      input form */
    $('label').addClass('control-label');
    //every input has a parent of div controls
    for(var i=1, j=$searchForm.length; i<j; i+=2) {
       $searchForm.slice(i, i+2).wrapAll('<div class="control-group"/>')
    }
    $('.input').wrap('<div class="controls"/>');
}


function searchPreview() {
    //refresh the description
    var $preview = $('#tft-search-preview');
    $preview.children().remove();
    var $dl = $('<dl></dl>');
    $dl.append('<h4>Preview</h4>');
    $dl.addClass('dl-horizontal');
    for (var i=0; i < INPUT_NAME.length; i++) {
        var inputVal = $('#'+INPUT_NAME[i][0]).val();
       // console.log(inputVal);
        if($.trim(inputVal)!='') {
            $dl.append('<dt>'+INPUT_NAME[i][1]+': </dt>');
            $dl.append('<dd>'+inputVal+'</dd>');
        }
    }
    $preview.append($dl);
}


function ajaxSearch () {
    $.post('/', $('#tft-search-form').serialize(), function (data) {
        console.log("Called ajaxSearch");
        //clear the search result for ready for next search result
        $('#search-results').children().remove()
        //create a table here
        var table = $('<table></table>').addClass('table table-condensed table-striped table-hover');
        var thead = $('<thead></thead>');
        var tbody = $('<tbody></tbody>');
        //Make sure we print the heading when the results returns values
        if (data.length > 0){
            printTHead(thead);
            for (var i = 0; i < data.length; i++) {
                printTBody(tbody, data[i]);
            }
            table.append(thead);
            table.append(tbody);
            $('#search-results').append(table);
        }
    }, 'json');
}


$(document).ready(function () {
    console.log("Loading jQuery, jQuery UI, and our own custom js!!!");
    $.ajaxSetup({traditional: true});
    initSearchForm ();
    addEventHandlers();
});


function addEventHandlers() {
    $('#tft-search-btn').click(ajaxSearch);
    $('.input-text').keypress(function (e) {
        if (e.which == 13) {
            console.log('enter pressed');
            ajaxSearch();
        }
    });
    $('.input-select').change(ajaxSearch);
}
