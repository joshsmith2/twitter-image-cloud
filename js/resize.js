/*
    Resize images dependant on how often they appear (this passed to the
    script as a seperate element)
 */

window.ResizeModule = {};

$(function() {

    //Return a tuple containing the highest count, and the id of the element
    //which has it
    var get_max_count = function(){
        var counts = [];
        $( 'img' ).each(function(){
            counts[counts.length] = $( this ).siblings('.count').text()
        });
        // Find max count
        return Math.max.apply(Math,counts);
    };

    var resize_divs = function(){
        var max_count = get_max_count();
        var max_width = 300;
        $('.packery-item').each(function(){
            var count = $( this ).children('.count').text();
            var new_width = Math.round(((count / max_count) * max_width) + 40);
            $(this).width(new_width);
        });
    };

    var repack = function(packery_instance){
        imagesLoaded( container, function() {
            packery_instance.layout();
        })
    };

    var make_draggable = function(packery_instance){
        var items = packery_instance.getItemElements();
        for ( var i=0, len = items.length; i < len; i++ ) {
            var item = items[i];
            var a_drag = new Draggabilly( item );
            packery_instance.bindDraggabillyEvents( a_drag );
        }
    };

    var limit_visible = function(visible_imgs){
        // Set default value to 500, if none given
        visible_imgs = typeof visible_imgs !== "undefined" ? visible_imgs : 300;
        // This is the prefix we're using for the Packery items.
        prefix = 'item';
        $('.packery-item').each(function(){
            var rank = parseInt($(this).attr('id').substr(prefix.length));
            if (rank > visible_imgs){
                $(this).hide();
                $(this).removeClass('packery-item');
            }
        });

    };

    // Return functions for use in unit tests
    ResizeModule.resize_divs = resize_divs;
    ResizeModule.get_max_count = get_max_count;
    ResizeModule.repack = repack;
    ResizeModule.limit_visible = limit_visible;
    ResizeModule.make_draggable = make_draggable;
});

$(document).ready(function(){
    ResizeModule.limit_visible(200);
    ResizeModule.resize_divs();
    var packery_item_selector = '.packery-item';
    var container = document.querySelector('#container');
    var pckry = new Packery( container, {
        itemSelector: packery_item_selector,
        gutter: 3
    });
    ResizeModule.make_draggable(pckry);
    ResizeModule.repack(pckry);
});