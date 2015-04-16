/*
    Resize images dependant on how often they appear (this passed to the
    script as a seperate element)
 */

//Declare functions in global scope, for testing


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



    var get_widths = function(){
        var widths = [];
        $( 'img' ).each(function(){
            widths[widths.length] = $( this ).width();
        });
        return widths;
    };

    // Return functions for use in unit tests
    ResizeModule.get_widths = get_widths;
    ResizeModule.get_max_count = get_max_count;
});

$(document).ready(function(){
});