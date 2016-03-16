function bindAdvanced(){
    $("#show_advanced").off("click").click(function(){
        if (($('#supersearch')).is(':hidden')){
            $(this).html('收起高级搜索');
            $("#supersearch").css('display', 'block');
        }
        else{
            $(this).html('高级搜索');
            $("#supersearch").css('display', 'none');
        }
    });
}
function base_call_ajax_request(url, callback){
    $.ajax({
        url:url,
        type:"get",
        dataType: "json",
        async: true,
        success: callback
    })
}
function draw_value_option(data){
    //console.log(data);
    if (data == 'no attribute'){
        data = [];
    }
    $('[name=tag_name]').empty();
    var html = '';
    for (var i=0;i<data.length;i++){
        html += '<option value="' + data[i] + '">' + data[i] + '</option>';
    }
    $('[name=tag_name]').html(html);
}

function getAttributeName(){
    var attribute_name_url = '/tag/show_attribute_name/';
    base_call_ajax_request(attribute_name_url, draw_name_option);
    function draw_name_option(data){
        // console.log(data);
        $('[name=tag_type]').empty();
        var html = '';
        html += '<option value="" checked>不限</option>';
        for (var i=0;i<data.length;i++){
            html += '<option value="' + data[i] + '">' + data[i] + '</option>';
        }
        $('[name=tag_type]').html(html);
        /*
        var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
        attribute_value_url += data[0];
        base_call_ajax_request(attribute_value_url, draw_value_option);
        */
        $('[name=tag_type]').change(function(){
            var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
            attribute_value_url += $(this).val();
            base_call_ajax_request(attribute_value_url, draw_value_option);
        });
    }
}
getAttributeName();
bindAdvanced();
