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
        $('.masonry-item').each(function(){
            var count = $( this ).children('.count').text();
            var new_width = Math.round(((count / max_count) * max_width) + 40);
            $(this).width(new_width);
        });
    };

    // Return functions for use in unit tests
    ResizeModule.resize_divs = resize_divs;
    ResizeModule.get_max_count = get_max_count;
});

$(document).ready(function(){
    ResizeModule.resize_divs();
    var container = document.querySelector('#container');

    // Packery
    var pckry = new Packery( container, {
      // options
        itemSelector: '.packery-item',
        gutter: 3
    });
    imagesLoaded( container, function() {
        pckry.layout();
    })


});