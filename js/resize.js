/*
    Resize images dependant on how often they appear (this passed to the
    script as a seperate element)
 */

//Declare functions in global scope, for testing


window.ResizeModule = {};

$(function() {

    var get_widths = function(){
        var widths = [];
        $( 'img' ).each(function(){
            widths[widths.length] = $( this ).width();
        });
        return widths;
    };

    ResizeModule.get_widths = get_widths
});

$(document).ready(function(){
});