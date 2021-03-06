/*
    Resize images dependant on how often they appear (this passed to the
    script as a seperate element)
 */

window.ResizeModule = {};
window.mode = 'drag';
window.prev_mode = 'drag';

$(function() {

    //Return a tuple containing the highest count, and the id of the element
    //which has it
    var get_max_count = function(){
        var counts = [];
        $('.count').each(function(){
            counts[counts.length] = $( this ).text()
        });
        // Find max count
        return Math.max.apply(Math,counts);
    };

    var resize_divs = function(){
        var max_count = get_max_count();
        var max_width = 300;
        $('.packery-item').each(function(){
            var count = $( this ).find('.count').text();
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
        // Set default value if none given
        visible_imgs = typeof visible_imgs !== "undefined" ? visible_imgs : 500;
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

    var make_items_pinnable = function(packery_instance, pin_selector){
        pin_selector = typeof pin_selector !== "undefined" ? pin_selector : '.pin';
        $(pin_selector).click(function(){
            var parent = $(this).parent();
            if ($(parent).hasClass('stamped')){
                packery_instance.unstamp(parent);
                $(parent).removeClass('stamped');
            }else{
                packery_instance.stamp(parent);
                $(parent).addClass('stamped');
            }
        });
    };

    var make_images_expandable = function(){
        $('.packery-item').dblclick(function(){
            if ($(this).hasClass('expanded')){
                $(this).removeClass('expanded');
            }else{
                $(this).addClass('expanded');
                $(this).find('.image-buttons').removeClass('hidden')
            }
        });
    };

    /* One place to handle all the things we need to do when changing window
       mode. If change_to given, change to current mode to this.
        Otherwise, just swap them.*/
    var change_window_mode = function(change_to) {
        if (typeof change_to !== "undefined"){
            window.prev_mode = window.mode;
            window.mode = change_to;
        }else {
            // Swap window.mode and window.prev_mode
            middleman = window.mode;
            window.mode = window.prev_mode;
            window.prev_mode = middleman;
        }
        if (window.mode == 'merge') {
            $('#merge-buttons').removeClass('hidden');
        } else {
            $('#merge-buttons').addClass('hidden');
            $('.packery-item').each(function () {
                $(this).removeClass('merge-alpha');
                $(this).removeClass('merge-candidate');
                $(this).removeClass('merge-selected');
            });
        }
    };

    var bind_mode_change_to_merge_buttons = function(packery_instance){
        $('button.merge').click(function(){
            if (window.mode != 'merge') {
                change_window_mode('merge');
                $(this).parent().removeClass('merge-candidate');
                $(this).parent().addClass('merge-alpha');
            }else{
                // If this is clicked on the alpha, cancel merge.
                // Otherwise, switch new element to alpha
                if ($(this).parent().hasClass('merge-alpha')){
                    change_window_mode();
                }else{
                    $('.packery-item').each(function(){
                        $(this).removeClass('merge-alpha');
                    });
                    $(this).parent().addClass('merge-alpha');
                }
            }
        });
        $('#cancel-merge').click(function(){
            change_window_mode();
        });
        $('#complete-merge').click(function(){
            var alpha_element = $('.merge-alpha').first();
            var sum = 0;
            sum += parseInt($(alpha_element).find('.count').text());
            $('.merge-selected').each(function(){
                var food_count = parseInt($(this).find('.count').text());
                sum += food_count;
                packery_instance.remove($(this));
            });
            $(alpha_element).find('.count').text(sum.toString());
            change_window_mode();
            resize_divs();
            repack(packery_instance);
        });
    };

    var bind_merge_mode_mouse_actions = function(){
        var packery_item = $('.packery-item');
        $(packery_item).mouseover(function(){
            if ($(this).hasClass('expanded')){
                $(this).find('.image-buttons').removeClass('hidden');
            }
            if (window.mode == 'merge'){
                $(this).addClass('merge-candidate');
            }
        });
        $(packery_item).mouseleave(function(){
            $(this).removeClass('merge-candidate');
            $(this).find('.image-buttons').addClass('hidden');
        });
        $(packery_item).click(function(event){
            if (window.mode == 'merge') {
                if ($(this).hasClass('merge-selected')) {
                    $(this).removeClass('merge-selected');
                } else {
                    var merge_button = $(this).find('button.merge').get(0);
                    if (event.target != merge_button){
                        $(this).addClass('merge-selected');
                    }
                }
            }
        });
    };

    var bind_hide_button_mouse_events = function(){
        var unhide_button = $('#unhide-all-images');
        $('button.hide').click(function(){
            image = $(this).parent().siblings('img');
            $(image).toggleClass('hidden');
            $(image).toggleClass('selected-for-hiding');
        });
        $(unhide_button).click(function(){
            $('.selected-for-hiding').toggleClass('hidden');
        });
    };

    // MAIN MENU
    var bind_main_menu_actions = function(){
        var main_menu_button = $('#open-main-menu');
        var main_menu = $('#main-menu');
        $(main_menu_button).click(function(){
            $(this).addClass('hidden');
            $(main_menu).removeClass('hidden');
        });
        $(main_menu).find('.close').first().click(function(){
            $(main_menu).addClass('hidden');
            $(main_menu_button).removeClass('hidden');
        });
        $(main_menu).children('button').click(function(){
            $(this).toggleClass('selected');
        });
    };

    var bind_blackout_curtain = function(){
        $('#drop-curtain').click(function(){
            $('#blackout-curtain').toggleClass('dropped');
        });
    };


    // Return functions for use in unit tests as well as on doc load
    ResizeModule.resize_divs = resize_divs;
    ResizeModule.get_max_count = get_max_count;
    ResizeModule.repack = repack;
    ResizeModule.limit_visible = limit_visible;
    ResizeModule.make_draggable = make_draggable;
    ResizeModule.make_items_pinnable = make_items_pinnable;
    ResizeModule.make_images_expandable = make_images_expandable;
    ResizeModule.change_window_mode = change_window_mode;
    ResizeModule.bind_mode_change_to_merge_buttons = bind_mode_change_to_merge_buttons;

    bind_merge_mode_mouse_actions();
    bind_main_menu_actions();
    bind_blackout_curtain();
    bind_hide_button_mouse_events();
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
    // Remove the divs of any images which fail to load from the DOM
    $(".packery-item img").each(function(){
        $(this).error(function(){
            var _parent = $(this).parent();
            pckry.remove(_parent);
        });
    });

    ResizeModule.bind_mode_change_to_merge_buttons(pckry);
    ResizeModule.make_images_expandable();

    ResizeModule.make_items_pinnable(pckry);
    ResizeModule.make_draggable(pckry);
    ResizeModule.repack(pckry);
});