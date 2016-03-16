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
function draw_conditions(url){
    $("#search_result").css("margin-top", "40px");
    $('#conditions').empty();
    var html = '';
    var pre_name = 'uname';
    var pre_value = 'test';

    var fix_result = process_par(pre_name, pre_value);
    //console.log(fix_result);
    var fix_name = fix_result[0];
    var fix_value = fix_result[1];
    // console.log(fix_name);
    // console.log(fix_value);
    if (fix_value){
        if (fix_value.indexOf(',') >= 0){
            var term_list = fix_value.split(',');
            for (var j = 0; j < term_list.length;j++){
                html += '<span class="mouse" id=choose_' + pre_name + '_' + j +' style="margin-left:10px">'+ fix_name + ':'+ term_list[j];
                html += '&nbsp;<a class="cross" href="#">X</a></span>';
            }
        }
        else{
            html += '<span class="mouse" id=choose_' + pre_name + ' style="margin-left:10px">'+ fix_name + ':'+ fix_value;
            html += '&nbsp;<a class="cross" href="#">X</a></span>';
        }
    }
    $('#conditions').html(html);
    return;
}
function process_par(name, value){
    var result = new Array();
    if (name == 'uid'){
        result[0] = '用户ID';
        result[1] = value;
    }
    else if(name=='uname'){
        result[0] = '昵称';
        result[1] = value;
    }
    else if(name=='location'){
        result[0] = '注册地';
        result[1] = value;
    }
    else if(name=='keywords'){
        result[0] = '关键词';
        result[1] = value;
    }
    else if(name=='hashtag'){
        result[0] = 'hashtag';
        result[1] = value;
    }
    else if(name=='psycho_status_by_emotion'){
        result[0] = '性格（语言）';
        result[1] = value;
    }
    else if(name=='psycho_status_by_word'){
        result[0] = '性格（情绪）';
        result[1] = value;
    }
    else if(name=='domain'){
        result[0] = '领域';
        result[1] = value;
    }
    else if(name=='topic'){
        result[0] = '话题';
        result[1] = value;
    }
    else if(name=='tag'){
        result[0] = '标签';
        result[1] = '';
        var term_list = value.split(',');
        for (var i = 0;i < term_list.length;i++){
            result[1] += (term_list[i].replace(':', '--') + ',');
        }
        result[1] = result[1].substring(0, result[1].length-1);
    }
    else{
        result[0] = '';
        result[1] = '';
    }
    return result;
}
function get_simple_par(){
    var str = '&uname=' + $('#uname').val();
    return str
}
function get_advanced_par(){
    var temp='';
    var input_value;
    var input_name;
    $('.ad-search').each(function(){
        input_name = '&' + $(this).attr('name');
        input_value = '=' + $(this).val();
        temp += input_name;
        temp += input_value;;
    });
    
    var psycho_status_by_emotion = new Array();
    $("[name='psycho_status_by_emotion']:checked").each(function(){
        psycho_status_by_emotion.push($(this).val());
    });
    temp += '&psycho_status_by_emotion=' + psycho_status_by_emotion.join(',');
    
    var psycho_status_by_word = new Array();
    $("[name='psycho_status_by_word']:checked").each(function(){
        psycho_status_by_word.push($(this).val());
    });
    temp += '&psycho_status_by_word=' + psycho_status_by_word.join(',');
    
    var domain = new Array();
    $("[name='domain']:checked").each(function(){
        domain.push($(this).val());
    });
    temp += '&domain=' + domain.join(',');

    var topic = new Array();
    $("[name='topic']:checked").each(function(){
        topic += $(this).val() + ',';
    });
    temp += '&topic=' + topic.join(',');

    temp += '&tag=' + $('[name="tag_type"]').val();
    temp += ':' + $('[name="tag_name"]').val();

    return temp;
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
