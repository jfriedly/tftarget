/**
   This is a collection of JavaScript functions.
   @authors - Djenome Team - Tremayne Mushayahama, Joel Friedly, Grant Michalski, Edward Powell
   @primary author - Tremayne Mushayahama
   @date 2/7/2013
*/

//TODO(jfriedly):  Add a spinner when a user clicks on 'Download all pages'.
//TODO(jfriedly):  Figure out why the link to download a CSV isn't in blue and fix it.
//TODO(jfriedly):  Make the download window close when you click the link.

// ________________________________________________________________
// |-------------------------CONSTANTS ----------------------------|
// `````````````````````````````````````````````````````````````````

var DEBUG = true;
/** Search results displayed on one page. The lower the number the
    faster the load time. Preferred results is in the
    range 50 <= RESULTS_PER_PAGE <= 500
*/
var RESULTS_PER_PAGE = 100;
var PAGINATION_NEXT = 'Next';
var PAGINATION_PREV = 'Prev';
var TF_LIST, SPECIES_LIST, EXPT_TYPE_LIST;
/**
   Used to order the column of the table. The purpose of the multidimensional array is to
   map from DB name to Human readable format
   e.g. expt_type - Experimental Type
*/
var TABLE_HEADING = [["transcription_factor", "Transcription Factor"],
                     ["gene", "Human Gene", 'human'],
                     ["gene", "Mouse Gene", 'mouse'],
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
    if (DEBUG) {
        console.log("Loading search.js...");
    }
    $.ajaxSetup({traditional: true});
    TF_LIST = $.parseJSON($('#tf-choices').html())
    SPECIES_LIST = $.parseJSON($('#tft-species').html());
    EXPT_TYPES_LIST = $.parseJSON($('#tft-expt-types').html())
    initTab(2);// tab 2 is the  first
});
/*Initialize all the commponets. All the 3 main forms of the have the same format
*/
function initTab(tabIndex) {
    if (tabInitialized[tabIndex]==false) {
        initForm('#tft-search-form-'+tabIndex);
        initMultiSelect('#tft-species-dropdown-'+tabIndex, SPECIES_LIST, 'species'+tabIndex);
        initMultiSelect('#tft-expt-types-dropdown-'+tabIndex,EXPT_TYPES_LIST, 'expt-types'+tabIndex);
        initTFControl('#tft-family-accordion-'+tabIndex, TF_LIST, tabIndex);
        
        addTabEvents(tabIndex);
        addPopoverEvents(tabIndex);
        addOnMouseOverEvents();
        tabInitialized[tabIndex]=true;
    }
}
/*InitForm ===========================================
 * Initializes the search and put all controls. Adds bootstrap class to rearrange and prettify the form 
 * labels and cotrols
 * @requires the form should have the format
 *   <form>
 *     <label></label>
 *     <controls>
 *     <label></label>
 *     <controls>
 *     ...
 *   </form>
 * @params formId -The id of the form */
function initForm (formId) {
    var $tftForm = $(formId).children(':not(:hidden)'); //get all non hidden components
    $(formId+' > label').addClass('control-label');
    //put a parent div to all non hidden components with a control-group class for bootstrap
    for(var i=0, j=$tftForm.length; i<j; i+=2) {
        $tftForm.slice(i, i+2).wrapAll('<div class="control-group span5"/>')
    }
    $(formId+' :input:not(:hidden)').wrap('<div class="controls " />');//wraps every input which is not hidden
}

/*Initialize the transcription factor dropdown.
*/
function initTFControl(accordionId, trans, tab) {
    for (var i = 0; i<trans.length; i++) {
        var familyId = trans[i][0]+tab;
        var $inner = $('<div/>');
        
        $(accordionId)
            .append($("<div/>")
                    .append($('<div/>') //Transcription Family Heading
                            .addClass('accordion-heading tft-family-heading')
                            .append($('<a/>')
                                    .addClass ('tft-white-btn accordion-toggle tft-family-toggle')  
                                    .attr('data-toggle', 'collapse')
                                    .attr('data-parent', accordionId)
                                    .attr('data-target', '#collapse'+familyId)
                                    .text(trans[i][0])
                                    .prepend("&nbsp;&nbsp;&nbsp;")
                                    .prepend($('<input id="'+familyId+'"type="checkbox" />')
                                             .addClass('tft-family-select')
                                             .attr('tft-parent-id', '#collapse'+ familyId))))
                    .append($('<div/>') //Body
                            .addClass('accordion-group')
                            .append( $('<div/>')
                                     .addClass('accordion-body collapse tft-accordion-container')
                                     .attr('id', 'collapse'+familyId)
                                     .append($inner))));
        
        for (var j= 1; j< trans[i].length; j++) {
            $inner
                .addClass('accordion-inner ')
                .append($('<li/>')
                        .append($('<label/>')
                                .addClass('checkbox')
                                .text(trans[i][j])
                                .append($('<input type="checkbox">')
                                        .addClass('family-member '+familyId) 
                                        .attr('my-parent', familyId)
                                        .attr('value', trans[i][j]))));
        }
    }
}

function initMultiSelect(container, tftList, listClass) {
    //put the select all
    $(container)
        .append($('<li/>')
                .append($('<label/>')
                        .text('Select All')
                        .addClass('checkbox')
                        .append($('<input type="checkbox">')
                                .addClass('tft-search-select-all')
                                .attr('select-target', listClass))));

    for (var i=1; i<tftList.length; i++) {
        $(container)
            .append($('<label/>')
                    .text(tftList[i][1])
                    .addClass('checkbox')
                    .append($('<input type="checkbox">')
                            .addClass(listClass)
                            .attr('value', tftList[i][1])));
    }
    $(container).click(function (e) {
        e.stopPropagation();
    });
}
// ________________________________________________________________
// |-------------------------SEARCH------ -------------------------|
// ````````````````````````````````````````````````````````````````
function ajaxSearch(url, rowNum, callback) {
    if (DEBUG) {
        console.log("AJAX searching!");
        console.log($('#tft-search-form-2').serialize())
    }
    $('#id_transcription_factor').val(writeJSON('family-member'));
    $('#id_expt_type').val(writeJSON('expt-types2'));
    $('#id_species').val(writeJSON('species2'));
    $('#id_row_index').val(rowNum);
    $.post(url, $('#tft-search-form-2').serialize(), function (data) {
        if (DEBUG) {
            console.log("AJAX searched");
            console.log(data);
        }
        callback(data);
    }, 'json');
}

function updatePage (url, rowNum, resetPagination) {
    if (DEBUG) {
        console.log('Called updatePage');
    }
    function createTable(data) {
        //clear the search result for ready for next search result
        $('#search-results').children().remove();
        //create a table here
        var table = $('<table></table>').addClass('table table-condensed table-striped table-hover');
        var thead = $('<thead></thead>').addClass('tft-grey-bottom-1');
        var tbody = $('<tbody></tbody>');

        var rows = data["num_results"];
        var results = data["results"];
        //differantiate searching by clicking page number of submit btn.
        //Submit btn should reset the page numbers shown starting from 1
        if (resetPagination==true) {
            paginate('#tft-page-container-top-2', 1, rows);
            paginate('#tft-page-container-bottom-2', 1, rows);
        }
        //Make sure we print the heading when the results returns values
        $('#tft-results-number-top-2').text(results.length + " results of " + rows);
        $('#tft-results-number-bottom-2').text(results.length + " results of " + rows);
        if (results.length > 0){
            $('#tft-result-container-2').show();
            printTHead(thead);
            for (var i = 0; i < results.length; i++) {
                printTBody(tbody, results[i], i+1);
            }
            table.append(thead);
            table.append(tbody);
            $('#search-results').append(table);
        } else {
            $('#tft-result-container-2').hide();
        }
    }
    ajaxSearch(url, rowNum, createTable);
}

function downloadDB(e) {
    e.preventDefault();
    ajaxSearch(e.target.href, 0, function (data) {
        if (DEBUG) {
            console.log("Opening download file dialog.");
        }
        $("#dialog").dialog({autoOpen: false, show: {
            effect: "blind",
            duration: 1
        }});
        $("#dialog").html('Your file can be downloaded from <a href="http://d.embolalia.net/' + data['url'] + '">here</a>');
        $("#dialog").dialog("open");
        //alert('Your file can be downloaded from <a href="http://d.embolalia.net/' +
        //      data["url"] + '">here</a>')
    });
}
/*Creates the page numbers. i.e. |Prev|3|4|5|Next
 * @params start The first page index to the left.
 * @params results the total number of rows
*/
function paginate(containerId, start, results) {
    $(containerId).children().remove();
    var pages = (results / RESULTS_PER_PAGE) + 1;//get the number of pages
    var pageSpan = start + 10;
    var $pagesContainer = $('<div/>').addClass('pagination tft-page-container ');
    var $pageList = $('<ul/>'); 
    for (var i=start; i<=pages && i<pageSpan; i++) {
        $pageList
            .append($('<li/>')
                    .attr('tft-page', i)
                    .addClass("tft-page-btn")
                    .append($('<a/>')
                            .text(i)));
    }
    // Determine to print "Previous" or "Next" Button
    if (start>1) {
        var $pageItem = $('<li class="tft-page-btn"><a>Prev</a></li>');
        $pageItem.attr('tft-page', PAGINATION_PREV);
        $pageItem.attr('tft-start-index', start);//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
        $pageItem.attr('tft-results', results);
        $pageList.prepend($pageItem);
    }
    if (pages>pageSpan) {
        var $pageItem = $('<li class="tft-page-btn"><a>Next</a></li>');
        $pageItem.attr('tft-page', PAGINATION_NEXT);
        $pageItem.attr('tft-start-index', start);//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
        $pageItem.attr('tft-results', results);
        $pageList.append($pageItem);
    }

    $pagesContainer.append($pageList);
    $(containerId).append($pagesContainer);
    addPageClickEvent();
}


/**This is a messed up function although it works
It is a temporary way to write json
*/
function writeJSON(cls) {
    var factors = '[';
    $('.' + cls + ':checked').each(function() {
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
    row += '<th class="tft-head tft-grey-bottom-1"></th>';
    for(var i=0; i < TABLE_HEADING.length; i++) {
       row += '<th class="tft-head tft-head tft-grey-bottom-1">' + TABLE_HEADING[i][1] + '</th>';
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
        if (property == 'gene') {
            row += '<td>' + object['gene'][ TABLE_HEADING[i][2]] + '</td>';//TABLE_HEADING[I][2] contains a second name in case it is ambiguous i.e. gene
        } else if (object[property]==null || object[property]=='') {
            row += '<td> - </td>'; //prints a desh to indicate no value
        } else if (property == 'pmid') {
            row += '<td><a target="blank" href="http://www.ncbi.nlm.nih.gov/pubmed/' + object[property] + '">' + object[property] + '</a></td>';
        } else if (property == 'gene') {
            row += '<td>' + object['gene']['human'] + '</td>';
            row += '<td>' + object['gene']['mouse'] + '</td>';
            i++;
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
function addTabEvents (tabIndex) {
    $('.tft-family-dropdown-menu').click(function (e) {
        e.stopPropagation();
    });
    addToggleEvents();
    addEventHandlers();
}
function addToggleEvents() {
    $(".tft-family-toggle").each(function () {
        $(this).click (function() {
            $($(this).attr('data-target')).collapse("toggle");
        });
    });
}
//function 
//fooo='p';
function addOnMouseOverEvents() {
    $("#tft-family-dropdown-toggle-2").mouseover(function(){
       // fooo=(writeJSON('family-member'));
        $("#tft-popover-tf-inner-2").text(writeJSON('family-member'));
    });
}
function addPopoverEvents(tabIndex) {
    $('#tft-family-dropdown-toggle-2').popover({ 
        trigger :'hover',
        title :'Selected Transcription Factor(s)',
        placement :'top',
        html : true,
        content: function() {
            return $('#tft-popover-tf-2').html();
        }
  });
}
function addPageClickEvent() {
    $('.tft-page-btn').click(function () {
        var pageVal = $(this).attr('tft-page');
        if (pageVal=="Prev") {
            var startIndex=parseInt($(this).attr('tft-start-index'));
            var results=parseInt($(this).attr('tft-results'));
            paginate('#tft-page-container-top-2', startIndex-1, results);
            paginate('#tft-page-container-bottom-2', startIndex-1, results);
        }else if (pageVal=="Next") {
            var startIndex=parseInt($(this).attr('tft-start-index'));
            var results=parseInt($(this).attr('tft-results'));
            paginate('#tft-page-container-top-2', startIndex+1, results);
            paginate('#tft-page-container-bottom-2', startIndex+1, results);
        } else {
            var rowNum = (parseInt(pageVal) - 1) * RESULTS_PER_PAGE;
            $(this).addClass('active');
            updatePage('/', rowNum, false);
        }
    });
}
function addEventHandlers() {
    $('.input-text').keypress(function (e) {
        if (e.which == 13) {
            if (DEBUG) {
                console.log('enter pressed');
            }
            updatePage('/', 0, true);//start at row 1
            //whenever someone presses enters, page 1 will be activated
            //resetPage(); will implement this
        }
    });
    //$('.input-select').change(updatePage(1));
    $('#tft-summary-btn-2').click(function (){
        $('#tft-summary-form-2').modal('show');
        searchSummary();
    });
    $('#tft-search-btn-2').click(function() {
        updatePage('/', 0, true);
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
    $('.tft-search-select-all').click(function() {
        if($(this).is(':checked')==true){
            $('.'+$(this).attr('select-target')).each(function(){
                this.checked = true;
            });
        } else {
            $('.'+$(this).attr('select-target')).each(function(){
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
    $('#tft-result-container-2').hide();
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
    $('.download-option').click(downloadDB)
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
