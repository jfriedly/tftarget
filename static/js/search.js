/**
   This is a collection of JavaScript functions.
   @authors - Djenome Team - Tremayne Mushayahama, Joel Friedly, Grant Michalski, Edward Powell
   @primary author - Tremayne Mushayahama
   @date 2/7/2013
*/

//FIXME(jfriedly): global variables sucks.

// ________________________________________________________________
// |-------------------------CONSTANTS ----------------------------|
// `````````````````````````````````````````````````````````````````

var DEBUG = true;
var TAB_NAMES = ["direct_targets", "enrichment_analysis", "query_db"];
/** Search results displayed on one page. The lower the number the
    faster the load time. Preferred results is in the
    range 50 <= RESULTS_PER_PAGE <= 500
*/
var RESULTS_PER_PAGE = 100;
var PAGINATION_NEXT = 'Next';
var PAGINATION_PREV = 'Prev';
var TF_LIST, SPECIES_LIST, EXPT_TYPE_LIST, TISSUE_LIST;
/**
   Used to order the column of the table. The purpose of the multidimensional array is to
   map from DB name to Human readable format
   e.g. expt_type - Experimental Type
*/
var TABLE_HEADING = [["transcription_factor", "Transcription Factor"],
                     ["gene", "Human Gene", 'human'],
                     ["gene", "Mouse Gene", 'mouse'],
                     ["gene", "Rat Gene", 'rat'],
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
    TISSUE_LIST = $.parseJSON($('#tft-tissue-choices').html());
    EXPT_TYPES_LIST = $.parseJSON($('#tft-expt-types').html())
    initTab(0);// tab 0 is the  first
});
/*Initialize all the commponets. All the 3 main forms of the have the same format
*/
function initTab(tabIndex) {
    if (tabInitialized[tabIndex]==false) {
        initForm('#tft-search-form-'+tabIndex);
        initMultiSelect('#tft-species-dropdown-'+tabIndex, SPECIES_LIST, 'species-'+TAB_NAMES[tabIndex], '#tft-species-summary-'+tabIndex);
        initMultiSelect('#tft-tissues-dropdown-'+tabIndex, TISSUE_LIST, 'tissues-'+TAB_NAMES[tabIndex], '#tft-tissues-summary-'+tabIndex);
        initMultiSelect('#tft-expt-types-dropdown-'+tabIndex, EXPT_TYPES_LIST, 'expt-types-'+TAB_NAMES[tabIndex], '#tft-expt-types-summary-'+tabIndex);
        initTFControl('#tft-family-accordion-'+tabIndex, TF_LIST, 'tf-'+tabIndex, '#tft-tf-summary-'+tabIndex, tabIndex);

        addTabEvents(tabIndex);
        addPopoverEvents();
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
function initTFControl(accordionId, trans, listClass,  tftSummaryView, tab) {
    for (var i = 0; i<trans.length; i++) {
        var familyId = trans[i][0]+'-'+TAB_NAMES[tab];
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
                                        .addClass('tft-tf-checkbox family-member '+familyId +' '+listClass)
                                        .attr('my-parent', familyId)
                                        .attr('tft-summary-target', tftSummaryView)
                                        .attr('value', trans[i][j]))));

        }
    }
}
function initMultiSelect(container, tftList, listClass, tftSummaryView) {
    //put the select all
    $(container)
        .append($('<li/>')
                .append($('<label/>')
                        .text('Select All')
                        .addClass('checkbox')
                        .append($('<input type="checkbox">')
                                .addClass('tft-search-select-all tft-checkbox')
                                .attr('tft-summary-target', tftSummaryView)
                                .attr('tft-list-class', listClass)
                                .attr('select-target', listClass))));

    for (var i=1; i<tftList.length; i++) {
        $(container)
            .append($('<label/>')
                    .text(tftList[i][1])
                    .addClass('checkbox')
                    .append($('<input type="checkbox">')
                            .addClass('tft-checkbox '+listClass)
                            .attr('tft-summary-target', tftSummaryView)
                            .attr('tft-list-class', listClass)
                            .attr('value', tftList[i][1])));
    }
    $(container).click(function (e) {
        e.stopPropagation();
    });
}
// ________________________________________________________________
// |-------------------------SEARCH------ -------------------------|
// ````````````````````````````````````````````````````````````````
function ajaxSearch(url, rowNum, callback, tabIndex) {
    if (DEBUG) {
        console.log("AJAX searching to " + url);
        console.log("Tab index: " + tabIndex + " (" + TAB_NAMES[tabIndex] + ")");
    }
    $('#id_transcription_factor.'+TAB_NAMES[tabIndex]).val(writeJSON('tf-'+tabIndex));
    $('#id_expt_type.'+TAB_NAMES[tabIndex]).val(writeJSON('expt-types-'+TAB_NAMES[tabIndex]));
    $('#id_species.'+TAB_NAMES[tabIndex]).val(writeJSON('species-'+TAB_NAMES[tabIndex]));
    $('#id_expt_tissues.'+TAB_NAMES[tabIndex]).val(writeJSON('tissues-'+TAB_NAMES[tabIndex]));
    $('#id_row_index.'+TAB_NAMES[tabIndex]).val(rowNum);
    if (DEBUG) {
        console.log($('#tft-search-form-'+tabIndex).serialize())
    }
    $.post(url, $('#tft-search-form-'+tabIndex).serialize(), function (data) {
        if (DEBUG) {
            console.log("AJAX searched");
            console.log(data);
        }
        callback(data);
    }, 'json');
}

function updatePage (url, rowNum, resetPagination, tabIndex) {
    if (DEBUG) {
        console.log('Called updatePage');
        console.log("Tab index: " + tabIndex + " (" + TAB_NAMES[tabIndex] + ")");
    }
    function createTable(data) {
        if (DEBUG) {
            console.log('Called createTable');
        }
        //clear the search result for ready for next search result
        $('#search-results-'+tabIndex).children().remove();
        //create a table here
        var table = $('<table></table>').addClass('table table-condensed table-striped table-hover');
        var thead = $('<thead></thead>').addClass('tft-grey-bottom-1');
        var tbody = $('<tbody></tbody>');

        var rows = data["num_results"];
        var results = data["results"];
        //differantiate searching by clicking page number of submit btn.
        //Submit btn should reset the page numbers shown starting from 1
        if (resetPagination==true) {
            paginate('#tft-page-container-top-'+tabIndex, 1, rows);
            paginate('#tft-page-container-bottom-'+tabIndex, 1, rows);
        }
        //Make sure we print the heading when the results returns values
        $('#tft-results-number-top-'+tabIndex).text(results.length + " results of " + rows);
        $('#tft-results-number-bottom-'+tabIndex).text(results.length + " results of " + rows);
        if (results.length > 0){
            $('#tft-result-container-'+tabIndex).show();
            printTHead(thead, TABLE_HEADING);
            for (var i = 0; i < results.length; i++) {
                printTBody(tbody, TABLE_HEADING, results[i], i+1);
            }
            table.append(thead);
            table.append(tbody);
            $('#search-results-'+tabIndex).append(table);
        } else {
            $('#tft-result-container-'+tabIndex).hide();
        }
    }
    ajaxSearch(url, rowNum, createTable, tabIndex);
}

function downloadDB(e) {
    ajaxSearch(e.target.href, 0, function (data) {
        if (DEBUG) {
            console.log("Opening download file dialog.");
        }

        $("#tft-download-status").text("Download Ready");
        $("#tft-download-progress").hide();
        $("#tft-download-link").show();
        $("#tft-download-link").attr("href", data['url']);
    }, 2);
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
    addPageClickEvent( $('.tab-pane.active').index());
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
function updateTranscriptionSummary(id, listClass, tabIndex) {
    $(id).children().remove();
    if (DEBUG) {
        console.log("ID clicked was: " + id);
    }
    var noSummary = true;
    $('.'+listClass+':checked').each(function() {
        var factor = $(this).attr('value');
        $(id).append($('<li/>')
                     .attr('id', 'tft-'+factor+'-container-'+tabIndex)
                     .append($('<ul/>')
                             .addClass('inline tft-summary-item-container')
                             .append($('<li/>')
                                     .addClass('tft-summary-item-name')
                                     .text(factor))
                             .append($('<li/>')
                                     .append($('<a/>')
                                             .addClass('tft-summary-item-remove')
                                             .click(function() {
                                                 $(this).parent().parent().parent().remove();
                                             })
                                             .text('X')))));
    });
}
function updateMultiSelectSummary(id, listClass, tabIndex) {
    $(id).children().remove();
    console.log(id);
    var noSummary = true;
    $('.' + listClass + ':checked').each(function() {
        var factor = $(this).attr('value');
        $(id).append($('<li/>')
                     .append($('<ul/>')
                             .addClass('inline tft-summary-item-container')
                             .append($('<li/>')
                                     .addClass('tft-summary-item-name tft-summary-'+listClass)
                                     .text(factor))
                             .append($('<li/>')
                                     .append($('<a/>')
                                             .addClass('tft-summary-item-remove')
                                             .attr('tft-list-class', listClass)
                                             .attr('tft-remove-target', factor)
                                             .click(function() {
                                                 $(this).parent().parent().parent().remove();
                                                 $('.'+listClass).each(function(){
                                                     if ($(this).attr('value')=='Mouse'){
                                                         $(this).checked = false;
                                                     }
                                                 });
                                             })
                                             .text('X')))));
    });
}
// ________________________________________________________________
// |-------------------------RESULTS-------------------------------|
// ````````````````````````````````````````````````````````````````
/**
   Prints the headings of the table from a json object. The result is appended to the table.
   @param thead - the thead element of the table
*/
function printTHead (thead, table_headers) {
    var row = '<tr>';
    //prints from heading according to the order of the TABLE_HEADING array.
    row += '<th class="tft-head tft-grey-bottom-1"></th>';
    for(var i=0; i < table_headers.length; i++) {
       row += '<th class="tft-head tft-head tft-grey-bottom-1">' + table_headers[i][1] + '</th>';
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
function printTBody (tbody, table_headers, object, rowNum) {
    var row = '<tr>';
    row += '<td>' + rowNum + '</td>';
    //prints from row according to the order of the TABLE_HEADING array.
    for (var i=0; i < table_headers.length; i++) {
        property = table_headers[i][0];
        if (property == 'gene') {
            row += '<td>' + object['gene'][table_headers[i][2]] + '</td>';//TABLE_HEADING[I][2] contains a second name in case it is ambiguous i.e. gene
        } else if (object[property]==null || object[property]=='') {
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
function addTabEvents (tabIndex) {
    $('.tft-family-dropdown-menu').click(function (e) {
        e.stopPropagation();
    });
    addToggleEvents(tabIndex);
    addEventHandlers(tabIndex);
}
function addToggleEvents(tabIndex) {
    $(".tft-family-toggle").each(function () {
        $(this).click (function() {
            $($(this).attr('data-target')).collapse("toggle");
        });
    });
}
function addOnMouseOverEvents(tabIndex) {
    $("#tft-family-dropdown-toggle-"+tabIndex).mouseover(function(){
       // fooo=(writeJSON('family-member'));
        $("#tft-popover-tf-inner-"+tabIndex).text(writeJSON('family-member'));
    });
}
function addPopoverEvents(tabIndex) {
    $('#tft-family-dropdown-toggle-'+tabIndex).popover({ 
        trigger :'hover',
        title :'Selected Transcription Factor(s)',
        placement :'right',
        html : true,
        content: function() {
            return $('#tft-popover-tf-'+tabIndex).html();
        }
  });
}
function addPageClickEvent(tabIndex) {
    $('.tft-page-btn').click(function () {
        var pageVal = $(this).attr('tft-page');
        if (pageVal=="Prev") {
            var startIndex=parseInt($(this).attr('tft-start-index'));
            var results=parseInt($(this).attr('tft-results'));
            paginate('#tft-page-container-top-'+tabIndex, startIndex-1, results);
            paginate('#tft-page-container-bottom-'+tabIndex, startIndex-1, results);
        }else if (pageVal=="Next") {
            var startIndex=parseInt($(this).attr('tft-start-index'));
            var results=parseInt($(this).attr('tft-results'));
            paginate('#tft-page-container-top-'+tabIndex, startIndex+1, results);
            paginate('#tft-page-container-bottom-'+tabIndex, startIndex+1, results);
        } else {
            var rowNum = (parseInt(pageVal) - 1) * RESULTS_PER_PAGE;
            $(this).addClass('active');
            updatePage('/'+TAB_NAMES[tabIndex], rowNum, false,  $('.tab-pane.active').index());
        }
    });
}
function enrichment_callback(data) {
    $('#search-results-1').children().remove();
    //create a table here
    var table = $('<table></table>').addClass('table table-condensed table-striped table-hover');
    var thead = $('<thead></thead>').addClass('tft-grey-bottom-1');
    var tbody = $('<tbody></tbody>');
    var table_headers = [['tf',         'Transcription Factor'],
                         ['enrichment', 'Enrichment']]
    $('#tft-result-container-1').show();
    printTHead(thead, table_headers);
    for (var i = 0; i < data.length; i++) {
        printTBody(tbody, table_headers, data[i], i+1);
    }
    table.append(thead);
    table.append(tbody);
    if (DEBUG) {
        console.log('Appending table');
    }
    $('#search-results-1').append(table);
}
function addEventHandlers(tabIndex) {
    //FIXME(jfriedly): We bind this event handler every time we initialize a
    //tab, so if a user looks at two tabs and then searches by pressing enter,
    //an AJAX request for each tab is made.
    $('.input-text.' + TAB_NAMES[tabIndex]).keypress(function (e) {
        if (e.which == 13) {
            e.preventDefault();
            if (DEBUG) {
                console.log('enter pressed');
            }
            updatePage('/'+TAB_NAMES[tabIndex], 0, true, tabIndex);//start at row 1
            //whenever someone presses enters, page 1 will be activated
            //resetPage(); will implement this
        }
    });
    $('#tft-clear-form-btn-'+tabIndex).click(function (){
        $('#tft-search-form-'+tabIndex).find('.tft-checkbox, .tft-tf-checkbox, .tft-family-select').each(function(){
            this.checked = false;
        });
        $('#tft-search-form-'+tabIndex).find('.tft-summary').children().remove();
        $('#tft-search-form-'+tabIndex).find('#id_gene_'+tabIndex).val(''); //sloppy code since all tabs doesn't have gene, but ehhh.
    });

    $('#tft-search-btn-'+tabIndex).click(function() {
        if (tabIndex == 1) {
            ajaxSearch('/'+TAB_NAMES[tabIndex], 0, enrichment_callback, tabIndex);
        } else {
            updatePage('/'+TAB_NAMES[tabIndex], 0, true, tabIndex);
        }
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
        updateTranscriptionSummary('#tft-tf-summary-'+tabIndex, 'tf-'+tabIndex, tabIndex);
    });
    $('.tft-tf-checkbox').click(function() {
        updateTranscriptionSummary($(this).attr('tft-summary-target'),'tf-'+tabIndex, tabIndex)
    });


   // updateTranscriptionSummary
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
        updateMultiSelectSummary($(this).attr('tft-summary-target'), 
                                 $(this).attr('tft-list-class'),
                                 tabIndex);
    });
    $('.tft-checkbox').click(function() {
        updateMultiSelectSummary($(this).attr('tft-summary-target'), 
                                 $(this).attr('tft-list-class'),
                                 tabIndex);
    }); 
    $('#tft-home-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        //choose the selected index
        initTab($('.tab-pane.active').index());
    })
    $('#tft-result-container-'+tabIndex).hide();
    $('#tft-download-bar').hide();
    //  $('#tft-summary-form-'+tabIndex).modal();
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

    var downloadOptionClick = function(e) {
        if (DEBUG) {
            console.log('A download option was clicked');
        }
        e.preventDefault()
        $("#tft-download-bar").show();
        $("#tft-download-modal").modal('show');
        $("#tft-download-status").text("Processing CSV ...");
        $("#tft-download-link").hide();
        $("#tft-download-progress").show();
        downloadDB(e);
    }

    $('.dropdown-toggle').dropdown();
    $('.download-option').unbind();
    $('.download-option').bind('click', downloadOptionClick);
    $("#tft-download-link").click(function () {
        $("#tft-download-modal").modal('hide');
    });
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
