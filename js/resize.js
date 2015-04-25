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

    var repack = function(){
        var container = document.querySelector('#container');
        var pckry = new Packery( container, {
            itemSelector: '.packery-item',
            gutter: 3
        });
        imagesLoaded( container, function() {
            pckry.layout();
        })
    };

    var limit_visible = function(visible_imgs){
        console.log("In limit");
        // Set default value to 500, if none given
        visible_images = typeof visible_imgs !== "undefined" ? visible_imgs : 500;
        // This is the prefix we're using for the Packery items.
        prefix = 'item';
        $('.packery-item').each(function(){
            var rank = parseInt($(this).attr('id').substr(prefix.length));
            console.log("Visible images: " + visible_imgs);
            console.log("Rank: " + rank);
            if (rank > visible_imgs){
                $(this).hide()
            }
        });

    };

    // Return functions for use in unit tests
    ResizeModule.resize_divs = resize_divs;
    ResizeModule.get_max_count = get_max_count;
    ResizeModule.repack = repack;
    ResizeModule.limit_visible = limit_visible;
});

$(document).ready(function(){
    ResizeModule.resize_divs();
    ResizeModule.limit_visible();
    ResizeModule.repack();
});