/**
   This is a collection of JavaScript functions. 
   @authors - Djenome Team - Tremayne Mushayahama, Joel Friedly, Grant Michalski, Edward Powell
   @primary author - Tremayne Mushayahama
   @date 2/7/2013
*/


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

/**
   Prints the headings of the table from a json object. The result is appended to the table.
   @param thead - the thead element of the table
*/
var tabInitialized = [false, false, false];
function printTHead (thead) {
    var row = '<tr>';
    //prints from heading according to the order of the TABLE_HEADING array.
    for(var i=0; i < TABLE_HEADING.length; i++) {
       row += '<th>' + TABLE_HEADING[i][1] + '</th>';
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
function printTBody (tbody, object) {
    var row = '<tr>';
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
/*Initialize all the commponets. All the 3 main forms of the have the same format
*/
function initializeTab(tabIndex) {
    if (tabInitialized[tabIndex]==false) {
        initializeForm('#tft-search-form-' + tabIndex);
        var trans = $.parseJSON($('#tf-choices').html())
        initializeTFControl('#tft-family-accordion-'+tabIndex, trans, tabIndex);
        tabInitialized[tabIndex]=true;
    }
    // This is to stop the drop down to hide when you click it
   
}
function initializeComponents() {
    $('.tft-family-dropdown-menu').click(function (e) {
        e.stopPropagation();
    });
    addToggleEvents();
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
function initializeForm (formId) {
    //get all hidden components
    var $tftForm = $(formId).children(':not(:hidden)');
    $(formId+' > label').addClass('control-label ');
    //wrap all non hidden components with a control-group class for bootstrap
    for(var i=0, j=$tftForm.length; i<j; i+=2) {
        $tftForm.slice(i, i+2).wrapAll('<div class="control-group span5"/>')
    }
    $(formId+' :input:not(:hidden)').wrap('<div class="controls " />');//wraps every input which is not hidden
}

/*Initialize the transcription factor dropdown. 
*/
function initializeTFControl(accordionId, trans, tab) {
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

function addToggleEvents() {
    $(".tft-family-toggle").each(function () {
        $(this).click (function() {
            $($(this).attr('data-target')).collapse("toggle");
        });
    });
   // $('#tft-close').click(function() {
     //   $('#tft-family-dropdown-toggle').click();
    //});
}



//will write a prettier code later
function searchSummary() {
    //refresh the description
    var $summary = $('#tft-summary-body');
    var factors = '';
    $summary.children().remove();
    $('.family-member:checked').each(function() {
        factors += $(this).attr('value') + ', '
    });
    
    var $dl = $('<dl></dl>');
    $dl.addClass('dl-horizontal');
    if($.trim(factors)!='') {
        $dl.append('<dt>Transcription Factor(s): </dt>');
        $dl.append('<dd>'+factors+'</dd>');
    }
    for (var i=0; i < INPUT_NAME.length; i++) {
        var inputVal = $('#'+INPUT_NAME[i][0]).val();
        if($.trim(inputVal)!='') {
            $dl.append('<dt>'+INPUT_NAME[i][1]+': </dt>');
            $dl.append('<dd>'+inputVal+'</dd>');
        }
    }
    $summary.append($dl);
}


function ajaxSearch () {
    console.log("AJAX searching!");
    $.post('/', $('#tft-search-form-2').serialize(), function (data) {
        console.log("AJAX searched");
        //clear the search result for ready for next search result
        $('#search-results').children().remove()
        //create a table here
        var table = $('<table></table>').addClass('table table-condensed table-striped table-hover');
        var thead = $('<thead></thead>').addClass('tft-thead');
        var tbody = $('<tbody></tbody>');
        //Make sure we print the heading when the results returns values
        $('#tft-results-number').text(data.length + " results");
        if (data.length > 0){
            $('#tft-download-db').show();
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
    initializeComponents ();
    initializeTab(2);// tab 2 is first
    addEventHandlers();
});
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
/*
All the event handlers that need to be loaded at ready are in this funtions.

/I will comment later
*/
function addEventHandlers() {
    $('.input-text').keypress(function (e) {
        if (e.which == 13) {
            console.log('enter pressed');
            ajaxSearch();
        }
    });
    $('.input-select').change(ajaxSearch);
    $('#tft-summary-btn-2').click(function (){
        $('#tft-summary-form-2').modal('show');
        searchSummary();
    });
    $('#tft-search-btn-2').click(function() {
        $('#id_transcription_factor').val(populateTranscriptionInput());
       // alert($('#id_transcription_factor').val());
        ajaxSearch();
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
        initializeTab($('.tab-pane.active').index());
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
