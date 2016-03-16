$('#commit_search').click(function(){
    if ($('#supersearch').is(':hidden')){
        var url = '/attribute/portrait_search/?stype=1';
        url += get_simple_par();
        console.log(url);
        base_call_ajax_request(url, draw_search_results);
    }
    else{
        var url = '/attribute/portrait_search/?stype=2';
        url += get_advanced_par();
        console.log(url);
        base_call_ajax_request(url, draw_search_results);
    }
});
function get_simple_par(){
    var str = '&uid=' + $('#uid').val();
    str += '&uname=' + $('#uname').val();
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
    
    var psycho_status_by_emotion_url = '&psycho_status_by_emotion=';
    $("[name='psycho_status_by_emotion']:checked").each(function(){
        if($(this).val()=='未知'){
            $(this).val() = '其他';
        }
        psycho_status_by_emotion_url += $(this).val() + ',';
    });
    temp += psycho_status_by_emotion_url;
    temp = temp.substring(0, temp.length-1);
    
    var psycho_status_by_word_url = '&psycho_status_by_word=';
    $("[name='psycho_status_by_word']:checked").each(function(){
        if($(this).val()=='未知'){
            $(this).val() = '其他';
        }
        psycho_status_by_word_url += $(this).val() + ',';
    });
    temp += psycho_status_by_word_url;
    temp = temp.substring(0, temp.length-1);
    
    var domain_url = '&domain=';
    $("[name='domain']:checked").each(function(){
        domain_url += $(this).val() + ',';
    });
    temp += domain_url;
    temp = temp.substring(0, temp.length-1);

    var topic_url = '&topic=';
    $("[name='topic']:checked").each(function(){
        topic_url += $(this).val() + ',';
    });
    temp += topic_url;
    temp = temp.substring(0, temp.length-1);

    temp += '&tag=' + $('[name="tag_type"]').val();
    temp += ':' + $('[name="tag_name"]').val();

    return temp;
}
function draw_search_results(data){
}
