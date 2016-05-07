

$(document).ready(function() {





     $("#edit_pane").on('keyup', "input[type='text']:not(.word_edit):not(.word_kun_edit)", function() {
        //alert("here here");
        //setTimeout(function() {alert($(this).val());}, 1);
        edit_id = ($(this).closest('.edit_item').attr('id'));
        //alert(edit_id)
        $("#" + edit_id +" ." + $(this).attr('name')).html($(this).val());
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
        var words_num = $(side_id + " input[name='words_num']").val();
        words_num++;
        $(side_id + " input[name='words_num']").val(words_num);
        //alert("before get");

        var chunk_id = words_num

        $.get('/tutor/get_chunk/', {template_name : 'word_edit_chunk.html',  chunk_id : chunk_id}, function(formData) {
            $(side_id + " .words_edit .add_word").before(formData);

        }).fail(function() { alert("cant reach the html file")});


        $.get('/tutor/get_chunk/', {template_name : 'word_field_chunk.html',  chunk_id : chunk_id}, function(fieldData) {
            $(side_id + " .words").append(fieldData);
        }).fail(function() { alert("cant reach the html file")});

    });

     $('#edit_pane').on('click', '.delete_word', function() {
        //alert("delete");

        var side_id = "#" + ($(this).closest('.edit_item').attr('id'));
        var field_id = $(this).parent().attr('id');
        var word_edit_item = $(this).parent()
        field_id = field_id.replace("edit_", "field_");
        //alert(field_id);

        //alert(word_edit_item);
        //alert(word_edit_item.attr('id'));
        //alert(field_id);
        word_field_item = $("#" + field_id);
        $(word_edit_item).remove();
        $(word_field_item).remove();
        var words_num = $(side_id + " input[name='words_num']").val();
        words_num--;
        $(side_id + " input[name='words_num']").val(words_num);


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
                alert("its okay");
            }

        })
        //alert(side_id);
    //alert(words_num);

    });

    $('#edit_pane').on('change', '.side_select', function() {

        var side_id = "#" + ($(this).closest('.edit_item').attr('id'));

        var template_name = $(this).val() + '_chunk.html';
        //alert(side_id + " " + template_name);
        var chunk_id = Math.floor(10 + Math.random() * (100))
        $.get('/tutor/get_chunk/', {template_name : template_name,  chunk_id : chunk_id}, function(sideData) {
            //alert(side_id);
            $(side_id).replaceWith(sideData);
            //alert(sideData);

        }).fail(function() { alert("cant reach the html file")});
    });






});