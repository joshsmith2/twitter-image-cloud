/*
    Resize images dependant on how often they appear (this passed to the
    script as a seperate element)
 */

//Declare functions in global scope, for testing

var ResizeModule = function($) {

    var test_brunion = "me";

    function get_widths(){
        var widths = [];
        $( img ).each(function(){
            widths[widths.length] = $( this ).width();
        });
        return widths;
    }

    return {
        test_brunion: test_brunion,
        get_widths: get_widths
    }
};

$(document).ready(function(){

});