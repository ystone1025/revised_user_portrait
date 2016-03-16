$('#commit_search').click(function(){
    if ($('#supersearch').is(':hidden')){
        var url = '/attribute/portrait_search/?stype=1';
        url += get_simple_par();
        console.log(url);
        //base_call_ajax_request(url, draw_search_results);
    }
    else{
        var url = '/attribute/portrait_search/?stype=2';
        url += get_advanced_par();
        console.log(url);
        //base_call_ajax_request(url, draw_search_results);
    }
});
function draw_search_results(data){
}
