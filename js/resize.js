/*
    Resize images dependant on how often they appear (this passed to the
    script as a seperate element)
 */



$(document).ready(function(){
    function get_widths(){
        var widths = [];
        $( img ).each(function(){
           widths[widths.length] = $( this ).width();
        });
        return widths;
    }
});