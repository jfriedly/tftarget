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
function prettifyForm (formId, tabIndex) {
    formId = formId+tabIndex;
    var $tftForm = $(formId).children(':not(:hidden)'); //get all non hidden components
    $(formId+' > label').addClass('control-label');
    //put a parent div to all non hidden components with a control-group class for bootstrap
    for(var i=0, j=$tftForm.length; i<j; i+=2) {
        $tftForm.slice(i, i+2).wrapAll('<div class="control-group span5"/>')
    }
    $(formId+' :input:not(:hidden)').wrap('<div class="controls " />');//wraps every input which is not hidden
}
/**
   Prints the headings of the table from a json object. The result is appended to the table.
   @param thead - the thead element of the table
*/
function printTHead (thead) {
    var row = '<tr>';
    //prints from heading according to the order of the TABLE_HEADING array.
    row += '<th class="tft-head tft-grey-bottom-thin"></th>';
    for(var i=0; i < TABLE_HEADING.length; i++) {
       row += '<th class="tft-head tft-head tft-grey-bottom-thin">' + TABLE_HEADING[i][1] + '</th>';
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
function addMultiSelect(container, tabIndex, tftList, listClass) {
    //put the select all
    listClass=listClass+tabIndex;
    container=container+tabIndex; 
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

function addMultiDropdown(accordionId, tabIndex, trans) {
    accordionId=accordionId+tabIndex;
    alert(accordionId);
    for (var i = 0; i<trans.length; i++) {
        var familyId = trans[i][0]+tabIndex;
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
