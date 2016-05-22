

$(document).ready(function() {



    $('#edit_pane').on('change', '.lvl_select', function() {
        $(".lvl").html($(this).val());
    });

     $("#edit_pane").on('keyup', "input[type='text']:not(.word_edit):not(.word_kun_edit):not(.lvl)", function() {
        //alert("here here");
        //setTimeout(function() {alert($(this).val());}, 1);
        edit_id = ($(this).closest('.edit_item').attr('id'));
        //alert(edit_id)
        $("#" + edit_id +" #" + $(this).attr('name')).html($(this).val());
    });

    //$("edit_pane").on('keyup')
    $('#edit_pane').on('keyup', '.word_edit', function() {
        var side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        var edit_element = $(this).parent().attr('id');
        var num = edit_element.match(/\d+/)[0];
        edit_element = edit_element.replace('edit_', 'field_');
        $("#" + edit_element + " .word").html(num + ") " + $(this).val());
    });

    $('#edit_pane').on('keyup', '.word_kun_edit', function() {
      var side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        var edit_element = $(this).parent().attr('id');
        var num = edit_element.match(/\d+/)[0];
        edit_element = edit_element.replace('edit_', 'field_');
        $("#" + edit_element + " .word_kun").html($(this).val());
    });



    $('#edit_pane').on('click', '.add_word', function() {
        var side_id = "#" + ($(this).closest('.edit_item').attr('id'));

        cardside = side_id.match(/\d+/)[0];
        var input_name = 'words_num_s' + cardside;
        var words_num = $(side_id + " input[name=" + input_name + "]").val();
        words_num++;
        $(side_id + " input[name=" + input_name + "]").val(words_num);

        var chunk_id = words_num;

        $.get('/tutor/get_chunk/', {template_name : 'word_edit_chunk.html',  chunk_id : chunk_id, cardside : cardside}, function(formData) {
            $(side_id + " .words_edit .add_word").before(formData);

        }).fail(function() { alert("cant reach the html file")});


        $.get('/tutor/get_chunk/', {template_name : 'word_field_chunk.html',  chunk_id : chunk_id, cardside : cardside}, function(fieldData) {
            $(side_id + " .words").append(fieldData);
        }).fail(function() { alert("cant reach the html file")});

    });

     $('#edit_pane').on('click', '.delete_word', function() {
        //alert("delete");

        var side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        cardside = side_id.match(/\d+/)[0];
        //alert(cardside);
        var field_id = $(this).parent().attr('id');
        var word_edit_item = $(this).parent()
        field_id = field_id.replace("edit_", "field_");
        word_field_item = $("#" + field_id);
        $(word_edit_item).remove();
        $(word_field_item).remove();
        var input_name = 'words_num_s' + cardside;
        var words_num = $(side_id + " input[name=" + input_name + "]").val();
        words_num--;
        $(side_id + " input[name=" + input_name + "]").val(words_num);
        //alert($(side_id + " input[name=" + input_name + "]").val());

        var delNum = field_id.match(/\d+/)[0];
        var wordEdits = $(side_id +  " .word_item_edit").toArray();
        var wordFields = $(side_id +  " .word_item_field").toArray();

        wordFields.forEach(function(wordField) {
            var id =  $(wordField).attr('id');
            var idNum = id.match(/\d+/)[0];
            if (idNum > delNum) {
                var newNum = idNum - 1;

                var current = $("#" + id + " .word").text();

                //alert("was" + id);
                var newId = id.replace(idNum, newNum);
                current = current.replace(idNum, newNum);

                $("#" + id + " .word").html(current);
                $("#" + id).attr('id', newId);
                //$(id + " .word_kun").attr('id', newId);
                //alert("now" + newId);
            }
            else {
                //alert("its okay");
            }
        })

        wordEdits.forEach(function(wordEdit) {

            var id = $(wordEdit).attr('id');
            var idNum = id.match(/\d+/)[0];
            if (idNum > delNum) {
                var newNum = idNum - 1;

                //alert("was" + id);
                var newId = id.replace(idNum, newNum);
                $("#" +  id).attr('id', newId);
                //$(id + " .word_kun").attr('id', newId);
                //alert("now" + newId);
            }
            else {
                //alert("its okay");
            }
        })
    });


    $('#edit_pane').on('click', '.delete_side', function() {
        //$("#edit_s1").attr('id', 'iHATEJAVASCRIPT');
        //alert(sides_num);
        //$('#edit_pane').append()
        var parent = $(this).closest('.edit_item');
        //alert($(parent).attr('id'));
        var del_side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        del_cardside = del_side_id.match(/\d+/)[0];
        del_side = $(del_side_id);
        $(parent).remove();
        var sides_array = $(".edit_item:not(.meta_edit)").toArray();
        var sides_num = sides_array.length;
        sides_array.forEach(function(side) {

            var side_id = $(side).attr('id');

            //alert($("#" + side_id + " input[name='pages[]']").val());
            var side_num = side_id.match(/\d+/)[0];
            if (side_num > del_cardside) {
                //alert($(side).html());
                var new_side_num = side_num - 1;
                var new_side_id = side_id.replace(side_num, new_side_num);
                //alert(new_side_id);

                $(side).attr('id', new_side_id);
                //alert($(side).html());
                var side_content = $('#' + new_side_id).html();
                //alert(side_content);
                var regex = /(\_s\d)/g;
                side_content = side_content.replace(regex, "_s" + new_side_num);
                $('#' + new_side_id).html(side_content);
                $('#' + new_side_id + " .sideinfo").html((new_side_num + 1) + "/" + sides_num);
            }
        })



     });



    $('#edit_pane').on('change', '.side_select', function() {

        var lvl = $("#info_lvl").val();
        var sides_number = $(".edit_item:not(.meta_edit)").length;

        //var card_info = {}; card_info.lvl = lvl; card_info.sides_number = sides_number;
        //alert(lvl + " " + sides_number);
        var side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        cardside = side_id.match(/\d+/)[0];
        var template_name = $(this).val() + '_chunk.html';
        //alert(side_id + " " + template_name);
        var chunk_id = -1;
        $.get('/tutor/get_chunk/', {template_name : template_name,  chunk_id : chunk_id,
                    cardside : cardside, lvl, sides_number}, function(sideData) {
            //alert(side_id);
            $(side_id).replaceWith(sideData);
            //alert(sideData);

        }).fail(function() { alert("cant reach the html file")});
    });

    $('#edit_pane').on('click', '.cardside_up, .cardside_down', function() {
        var side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        var cardside = side_id.match(/\d+/)[0];
        var new_side_number = -1;
        if ($(this).attr('class') == 'cardside_up') {
            new_side_number = cardside - 1;
        } else
        if ($(this).attr('class') == 'cardside_down') {
            new_side_number = Number.parseInt(cardside) + 1;
        }
        var side_content = $(side_id).html();
        var regex = /(\_s\d)/g;

        var editItems = $(".edit_item:not(.meta_edit)").toArray();

        editItems.forEach(function(editItem) {

            var edit_id = $(editItem).attr('id');
            idNum = edit_id.match(/\d+/)[0];

            //alert(idNum + " " + new_side_number)
            var changeStatus = false;
            if (idNum == new_side_number) {
                changeStatus = true;
                edit_content = $(editItem).html();
                side_content = side_content.replace(regex, "_s" + new_side_number);
                edit_content = edit_content.replace(regex, "_s" + cardside);
                $(editItem).html(side_content);
                $(side_id).html(edit_content);

                $(editItem).trigger('side_change');
                $(side_id).trigger('side_change');
                //break;
            }
            var alertString = "cardside: " + edit_id + "change status: " + changeStatus;

        });
        //var regex = new Regex((/([^\?]*)\_s(\d*)/))        //alert(match);
    });

    $('#edit_pane').on('side_change', ".edit_item", function() {
        //alert($(this).attr('id'));
        var side_id = "#" + $(this).attr('id');
        var cardside = $(side_id + " input[name='pages[]'").val();
        cardside = cardside.match(/\d+/)[0];
         cardside++;

        new_sideinfo = $(side_id + " .sideinfo").text();

        //alert($(this).attr('id'));
        new_sideinfo = new_sideinfo.replace(/(\d)/, cardside.toString());
        //alert(new_sideinfo)
        $(side_id + " .sideinfo").html(new_sideinfo);

    });

     $('#edit_pane').on('click', '.add_side_btn', function() {

        //var sides_array = $(".edit_item:not(.meta_edit)").toArray();
        //var side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        //var sides_num = sides_array.length;
        var cardside = $(".edit_item:not(.meta_edit)").length;
        var template_name = $("#new_side_select").val() + "_chunk.html";
        //alert(template_name);
        var lvl = $("#info_lvl").val();
        var sides_number = cardside + 1;
        $.get('/tutor/get_chunk/', {template_name : template_name,  cardside : cardside, lvl : lvl, sides_number : sides_number}, function(sideData) {
            $("#add_side").before(sideData);

        }).fail(function() { alert("cant reach the html file")});
        //$('#edit_pane').append()

     });





});