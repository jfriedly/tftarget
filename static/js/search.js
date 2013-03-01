/**
   This is a collection of JavaScript functions. 
   @authors - Djenome Team - Tremayne Mushayahama, Joel Friedly, Grant Michalski, Edward Powell
   @primary author - Tremayne Mushayahama
   @date 2/7/2013
*/



// ________________________________________________________________
// |-------------------------CONSTANTS ----------------------------|
// `````````````````````````````````````````````````````````````````

/** Search results displayed on one page. The lower the number the 
    faster the load time. Preferred results is in the 
    range 50 <= RESULTS_PER_PAGE <= 500
*/
var RESULTS_PER_PAGE = 100;
/**
   Used to order the column of the table. The purpose of the multidimensional array is to 
   map from DB name to Human readable format
   e.g. expt_type - Experimental Type
*/
var TABLE_HEADING = [["transcription_factor", "Transcription Factor"],
                     ["gene", "Gene"],
                     ["pmid", "PMID"],
                     ["species", "Species"],
                     ["expt_tissues", "Organ"],
                     ["cell_line", "Tissues/Cell Line"],
                     ["expt_type", "Experiment"]];

var INPUT_NAME = [["id_gene", "Gene"],
                  ["id_species", "Experimental Species"],
                  ["id_tissue_name", "Experimental Tissues"],
                  ["id_expt_type", "Experiment Type"]];

/*Shows which tabs are initialized */
var tabInitialized = [false, false, false];
/*__________________________________________________________________________________________________*/

// ________________________________________________________________
// |-------------------------INITIALIZATIONS-----------------------|
// `````````````````````````````````````````````````````````````````

$(document).ready(function () {
    console.log("Loading jQuery, jQuery UI, and our own custom js!!!");
    $.ajaxSetup({traditional: true});
    addEventHandlers();
    initTab(2);// tab 2 is first
    
});
/*Initialize all the commponets. All the 3 main forms of the have the same format
*/
function initTab(tabIndex) {
    if (tabInitialized[tabIndex]==false) {
        initForm('#tft-search-form-' + tabIndex);
        var species = $.parseJSON($('#tft-species').html());
        
      //  alert(species[1][1]);
        
        var trans = $.parseJSON($('#tf-choices').html())
        initTFControl('#tft-family-accordion-'+tabIndex, trans, tabIndex);
        $('.tft-family-dropdown-menu').click(function (e) {
            e.stopPropagation();
        });
        addToggleEvents();
        tabInitialized[tabIndex]=true;
    }
    // This is to stop the drop down to hide when you click it
   
}
/*Initializes the search and put all controls. 
@requires the form should have the format
<form> 
<label></label><controls>
<label></label><controls>
...
</form>
@params formId -The id of the form  
*/
function initForm (formId) {
    var $tftForm = $(formId).children(':not(:hidden)'); //get all hidden components
    $(formId+' > label').addClass('control-label ');
    //wrap all non hidden components with a control-group class for bootstrap
    for(var i=0, j=$tftForm.length; i<j; i+=2) {
        $tftForm.slice(i, i+2).wrapAll('<div class="control-group span5"/>')
    }
    $(formId+' :input:not(:hidden)').wrap('<div class="controls " />');//wraps every input which is not hidden
}

/*Initialize the transcription factor dropdown. 
*/
function initTFControl(accordionId, trans, tab) {
    var $familyAccordion = $(accordionId);
    for (var i =0; i<trans.length; i++) {
        var familyId = trans[i][0]+tab;
        var $familyGroup = $('<div></div>').addClass('accordion-group');
        var $familyHeading = $('<div></div>').addClass('accordion-heading tft-family-heading');
        var $familyToggle = $('<a></a>').addClass ('btn accordion-toggle tft-family-toggle ');
        var $familyNameCheckBox = $('<input id="'+familyId+'"type="checkbox" />').addClass('tft-family-select');
        var $collapse = $('<div></div>').addClass('accordion-body collapse');
        var $inner = $('<div></div>').addClass('accordion-inner');

        $familyToggle.attr('data-toggle', 'collapse');
        $familyToggle.attr('data-parent', $familyAccordion);
        $familyToggle.attr('data-target', '#collapse'+familyId);
        $familyToggle.text(trans[i][0]);

        $collapse.attr('id', 'collapse'+familyId);
        $familyNameCheckBox.attr('tft-parent-id', '#collapse'+ familyId);

        //appending
        $familyToggle.prepend("&nbsp;&nbsp;&nbsp;");
        $familyToggle.prepend($familyNameCheckBox);
        $familyHeading.append($familyToggle);
        $collapse.append($inner);
        $familyGroup.append($familyHeading);
        $familyGroup.append($collapse);

        for (var j= 1; j< trans[i].length; j++) {
            $familyMember = $('<li><label class="checkbox"><input type="checkbox" my-parent="'
                              +familyId+'" class="family-member '
                              +familyId+'" value="'+trans[i][j]+'">'
                              +trans[i][j]
                              +'</label></li>');
            $inner.append($familyMember);
        }
        $familyAccordion.append($familyGroup);
    }
   
}
function initMultiSelect(tftList) {
    for (var i=0; i<tftList.length; i++) {
    }
}
// ________________________________________________________________
// |-------------------------SEARCH------ -------------------------|
// ````````````````````````````````````````````````````````````````
function ajaxSearch (rowNum, resetPagination) {
    console.log("AJAX searching!");
    $.post('/', $('#tft-search-form-2').serialize()+ '&row_index='+rowNum +'&rows='+RESULTS_PER_PAGE, function (data) {
        console.log("AJAX searched");
        //clear the search result for ready for next search result
        $('#search-results').children().remove();
        //create a table here
        var table = $('<table></table>').addClass('table table-condensed table-striped table-hover');
        var thead = $('<thead></thead>').addClass('tft-thead');
        var tbody = $('<tbody></tbody>');
        
        //UNCOMMENT THIS CODE IF YOU FINISH IMPLEMENTING THE BACK
      /*  var rows = data["num_results"];
        var results = data["results"];
        //differantiate searching by clicking page number of submit btn.
        //Submit btn should reset the page numbers shown starting from 1
        if (resetPagination==true) {
            paginate(1, rows);
        }
        //Make sure we print the heading when the results returns values
        $('#tft-results-number').text(results.length + " results");
        if (results.length > 0){
            $('#tft-download-db').show();
            printTHead(thead);
            for (var i = 0; i < results.length; i++) {
                printTBody(tbody, results[i], i+1);
            }
            table.append(thead);
            table.append(tbody);
            $('#search-results').append(table);
        }
        */
        //DELETE THIS CODE BLOCK IF YOU FINISH IMPLEMENTING THE BACK
        //START BLOCK
        if (resetPagination==true) {
            paginate(1, 2145);//random number
        }
        //Make sure we print the heading when the results returns values
        $('#tft-results-number').text(data.length + " results");
        if (data.length > 0){
            $('#tft-download-db').show();
            printTHead(thead);
            for (var i = 0; i < data.length; i++) {
                printTBody(tbody, data[i], i+1);
            }
            table.append(thead);
            table.append(tbody);
            $('#search-results').append(table);
        }
        //END BLOCK
    }, 'json');
}
/*Creates the page numbers. i.e. |Prev|3|4|5|Next
  @params start The first page index to the left.
  @params results the total number of rows
*/ 
function paginate(start, results) {
    $('#tft-page-container-2').children().remove();
    var pages = results / RESULTS_PER_PAGE;//get the number of pages
    var pageSpan = start + 10;
    var $pagesContainer = $('<div></div>').addClass('pagination pagination-centered');
    var $pageList = $('<ul></ul>'); 
    for (var i=start; i<=pages && i<pageSpan; i++) {
        var $pageItem = $('<li class="tft-page-btn"><a>'+i+'</a></li>');
        $pageItem.attr('tft-page', i);
        $pageList.append($pageItem);
    }
    // Determine to print "Previous" or "Next" Button
    if (start>1) {
        var $pageItem = $('<li class="tft-page-btn"><a>Prev</a></li>');
        $pageItem.attr('tft-page', 'Prev');
        $pageItem.attr('tft-start-index', start);//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
        $pageItem.attr('tft-results', results);
        $pageList.prepend($pageItem);
    }
    if (pages>pageSpan) {
        var $pageItem = $('<li class="tft-page-btn"><a>Next</a></li>');
        $pageItem.attr('tft-page', 'Next');
        $pageItem.attr('tft-start-index', start);//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
        $pageItem.attr('tft-results', results);
        $pageList.append($pageItem);
    }
        
    $pagesContainer.append($pageList);
    $('#tft-page-container-2').append($pagesContainer);
    addPageClickEvent();
}


/**This is a messed up function although it works
It is a temporary way to write json 
*/
function populateTranscriptionInput() {
    var factors = '[';
    $('.family-member:checked').each(function() {
        factors += '"'+$(this).attr('value') + '",'
    });
    if (factors.length>1) {
        return factors.slice(0, -1)+']';
    } else {
        return ''; // so that it does not return [
    }
}

//will write a prettier code later
function searchSummary() {
    //refresh the description
    var $summary = $('#tft-summary-body');
    var factors = '';
    var noSummary = true;
    $summary.children().remove();
    $('.family-member:checked').each(function() {
        factors += $(this).attr('value') + ', '
    });
    
    var $dl = $('<dl></dl>');
    $dl.addClass('dl-horizontal');
    if($.trim(factors)!='') {
        $dl.append('<dt>Transcription Factor(s): </dt>');
        $dl.append('<dd>'+factors+'</dd>');
        noSummary = false;
    }
    for (var i=0; i < INPUT_NAME.length; i++) {
        var inputVal = $('#'+INPUT_NAME[i][0]).val();
        if($.trim(inputVal)!='') {
            $dl.append('<dt>'+INPUT_NAME[i][1]+': </dt>');
            $dl.append('<dd>'+inputVal+'</dd>');
            noSummary=false;
        }
    }
    if(noSummary==true) {
         $summary.append('<h5>no selected item(s) </h5>');
    } else {
        $summary.append($dl);
    }
}


// ________________________________________________________________
// |-------------------------RESULTS-------------------------------|
// ````````````````````````````````````````````````````````````````
/**
   Prints the headings of the table from a json object. The result is appended to the table.
   @param thead - the thead element of the table
*/
function printTHead (thead) {
    var row = '<tr>';
    //prints from heading according to the order of the TABLE_HEADING array.
    row += '<th class="tft-head"></th>';
    for(var i=0; i < TABLE_HEADING.length; i++) {
       row += '<th class="tft-head">' + TABLE_HEADING[i][1] + '</th>';
    }
    row += '</tr>' //close the table row
    thead.append(row);
}
/**
   Prints the rest of the table from a json object. The result is appended to the table.
   Make sure the printHead fuction order correspond to this function
   Every pmid is printed as a link to the PubMed Website. It opens in a new window
   If a value doesn't contain anything, a hyphen is printed.

   @param tbody - the tbody element of the table
   @param object - the json object
*/
function printTBody (tbody, object, rowNum) {
    var row = '<tr>';
    row += '<td>' + rowNum + '</td>';
    //prints from row according to the order of the TABLE_HEADING array.
    for (var i=0; i < TABLE_HEADING.length; i++) {
        property = TABLE_HEADING[i][0];
        if (object[property]==null || object[property]=='') {
             row += '<td> - </td>'; //prints a desh to indicate no value
        } else if (property == 'pmid') {
            row += '<td><a target="blank" href="http://www.ncbi.nlm.nih.gov/pubmed/' + object[property] + '">' + object[property] + '</a></td>';
        } else {
            row += '<td>' + object[property] + '</td>';
        }
    }
    row += '</tr>'; //end the row, ready to append
    tbody.append(row);
}

// ______________________________________________________________________
// |------------------------- EVENT HANDLERS ----------------------------|
//  ``````````````````````````````````````````````````````````````````````
/*Handles the event of the dropdown collapsible*/
function addToggleEvents() {
    $(".tft-family-toggle").each(function () {
        $(this).click (function() {
            $($(this).attr('data-target')).collapse("toggle");
        });
    });
}
function addPageClickEvent() {
    $('.tft-page-btn').click(function () {
        var pageVal = $(this).attr('tft-page');
        if (pageVal=="Prev") {
            var startIndex=parseInt($(this).attr('tft-start-index'));
            var results=parseInt($(this).attr('tft-results'));
            paginate(startIndex-1, results);
        }else if (pageVal=="Next") {
            var startIndex=parseInt($(this).attr('tft-start-index'));
            var results=parseInt($(this).attr('tft-results'));
            paginate(startIndex+1, results);
        } else {
            var rowNum = parseInt(pageVal) * RESULTS_PER_PAGE;
            ajaxSearch(rowNum, false);
        }
    });
}
function addEventHandlers() {
    $('.input-text').keypress(function (e) {
        if (e.which == 13) {
            console.log('enter pressed');
            ajaxSearch(1, true);//start at row 1
            //whenever someone presses enters, page 1 will be activated
            //resetPage(); will implement this
        }
    });
    //$('.input-select').change(ajaxSearch(1));
    $('#tft-summary-btn-2').click(function (){
        $('#tft-summary-form-2').modal('show');
        searchSummary();
    });
    $('#tft-search-btn-2').click(function() {
        $('#id_transcription_factor').val(populateTranscriptionInput());
       // alert($('#id_transcription_factor').val());
        ajaxSearch(1, true);
    });

    $('.tft-family-select').click(function() {
        $($(this).attr('tft-parent-id')).collapse('show');
        if($(this).is(':checked')==true){
            $('.'+$(this).attr('id')).each(function(){ 
                this.checked = true;
            });
        } else {
            $('.'+$(this).attr('id')).each(function(){ 
                this.checked = false;
            });
        }
    });
    $('#tft-home-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        //choose the selected index
        initTab($('.tab-pane.active').index());
    })
    $('#tft-download-db').hide();
  //  $('#tft-summary-form-2').modal();
  //  $('#tft-home-tab a[href="#download-database"]').click();
        /* $('.family-member').click(function() {
       // console.log('im a clicked member');
       // console.log( $('.'+$(this).attr('my-parent')).length);
         $('.'+$(this).attr('my-parent')).each(function(){ 
             if($(this).is(':checked')==false) {
                 $('#'+$(this).attr('my-parent')).attr("checked", "false");
             }
         });
    });*/
    $('.dropdown-toggle').dropdown();
}
$(function() {

    var tf = [
        "E2F",
        "MYC",
        "STAT",
        'Human',
        'Mouse',
        'Chip'
    ];
    function split( val ) {
        return val.split( /,\s*/ );
    }
    function extractLast( term ) {
        return split( term ).pop();
    }
    $( "#tft-search-query" )
    // don't navigate away from the field on tab when selecting an item
        .bind( "keydown", function( event ) {
            if ( event.keyCode === $.ui.keyCode.TAB &&
                 $( this ).data( "autocomplete" ).menu.active ) {
                event.preventDefault();
            }
        })
        .autocomplete({
            minLength: 0,
            source: function( request, response ) {
                // delegate back to autocomplete, but extract the last term
                response( $.ui.autocomplete.filter(
                    tf, extractLast( request.term ) ) );
            },
            focus: function() {
                // prevent value inserted on focus
                return false;
            },
            select: function( event, ui ) {
                var terms = split( this.value );
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push( ui.item.value );
                // add placeholder to get the comma-and-space at the end
                terms.push( "" );
                 this.value = terms.join( ", " );
                return false;
            }
        });
});
