
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
function paginate(containerId, start, results, pageNum) {
    $(containerId).children().remove();
    var pages = (results / RESULTS_PER_PAGE) + 1;//get the number of pages
    var pageSpan = start + 7;
    var $pagesContainer = $('<div/>').addClass('tft-page-container');
    var $pageList = $('<ul/>').addClass("nav nav-pills inline"); 
    for (var i=start; i<=pages && i<pageSpan; i++) {
        if (i==pageNum) {
            $pageList
                .append($('<li/>')
                        .attr('tft-page-value', i)
                        .attr('tft-start-index', start)//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
                        .attr('tft-results', results)
                        .append($('<a/>')
                                .addClass("tft-page-active")
                                .text(i)));
            
        } else {
            $pageList
                .append($('<li/>')
                        .attr('tft-page-value', i)
                        .addClass("tft-page-btn")
                        .attr('tft-start-index', start)//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
                        .attr('tft-results', results)
                        .append($('<a/>')
                                .text(i)));
        }
    }
    // Determine to print "Previous" or "Next" Button
    if (start>1) {
        var $pageItem = $('<li class="tft-page-btn"><a>Prev</a></li>');
        $pageItem.attr('tft-page-value', pageNum);
        $pageItem.attr('tft-page-name', PAGINATION_PREV);
        $pageItem.attr('tft-start-index', start);//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
        $pageItem.attr('tft-results', results);
        $pageList.prepend($pageItem);
    }
    if (pages>pageSpan) {
        var $pageItem = $('<li class="tft-page-btn"><a>Next</a></li>');
        $pageItem.attr('tft-page-value', pageNum);
        $pageItem.attr('tft-page-name', PAGINATION_NEXT);
        $pageItem.attr('tft-start-index', start);//indicates the btn value next to previous i.e |Prev|2|3|4.. val = 2
        $pageItem.attr('tft-results', results);
        $pageList.append($pageItem);
    }
    $pagesContainer.append($pageList);
    $(containerId).append($pagesContainer);
    
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
                                             .attr('tft-list-class', listClass)
                                             .attr('tft-remove-target', factor)
                                             .text('x')))));
    });
    $('.tft-summary-item-remove').click(function() {
        $(this).parent().parent().parent().remove();
        var removeTarget =  $(this).attr('tft-remove-target');
        $('.'+listClass).each(function(){
            if ($(this).attr('value')==removeTarget){
                this.checked = false;
            }
        });
    })
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
                                             .text('x')))));
    });
    $('.tft-summary-item-remove').click(function() {
        $(this).parent().parent().parent().remove();
        var removeTarget =  $(this).attr('tft-remove-target');
        $('.'+listClass).each(function(){
            if ($(this).attr('value')==removeTarget){
                this.checked = false;
            }
        });
    })
}