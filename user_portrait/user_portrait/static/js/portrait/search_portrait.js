$('#commit_search').click(function(){
    if ($('#supersearch').is(':hidden')){
        var url = '/attribute/portrait_search/?stype=1';
        url += get_simple_par();
    }
    else{
        var url = '/attribute/portrait_search/?stype=2';
        url += get_advanced_par();
    }
    console.log(url);
    draw_conditions(url);
    //base_call_ajax_request(url, draw_search_results);
});
function draw_search_results(data){
    $('#search_result').empty();
    var user_url ;
    //console.log(user_url);
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th>' + '<input name="choose_all" id="choose_all" type="checkbox" value="" onclick="choose_all()" />' + '</th></tr></thead>';
    html += '<tbody>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      item = replace_space(item);
      for(var j=3;j<7;j++){
        if(item[j]!='未知')
          item[j] = item[j].toFixed(2);
      }
      global_data[item[0]] = item; // make global data
      user_url = '/index/personal/?uid=' + item[0];
      html += '<tr id=' + item[0] +'>';
      html += '<td class="center" name="uids"><a href='+ user_url+ '  target="_blank">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] +'</td>';
      html += '<td class="center">'+ item[2] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[3] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[4] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[6] +'</td>';
      html += '<td class="center"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + item[0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#search_result').append(html);
}
function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}
