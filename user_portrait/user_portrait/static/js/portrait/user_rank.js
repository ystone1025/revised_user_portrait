function task_status (data) {
	var html = '';
	html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;width:900px;font-size:14px;">';
	for(var i=0;i<data.length;i++){
		html += '<tr>';
		html += '<td style="width:200px;text-align:center;">'+data[i][0]+'</td>';
		html += '<td>'+data[i][1]+'</td>';
		html += '</tr>';
	}
	html += '</table>';
	$('#task_status').append(html);
}

function draw_rank_table(data){
	$('#result_rank_table').empty();
	var html = '';
	html += '<table id="rank_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;width:900px;">';
	for(var i=0;i<data.length;i++){
		html += '<tr>';
		html += '<td style="width:200px;text-align:center;">'+data[i][0]+'</td>';
		html += '<td>'+data[i][1]+'</td>';
		html += '</tr>';
	}
	html += '</table>';
	$('#result_rank_table').append(html);
	$('#rank_table').dataTable({
		"sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
		"sPaginationType": "bootstrap",
		"aoColumnDefs":[ {"bSortable": false, "aTargets":[1]}],
		"oLanguage": {
		    "sLengthMenu": "_MENU_ 每页",
		}
    });
}


//排序范围选择
$('#range_choose').change(function(){
	$('#range_choose_detail').empty();
	if($('#range_choose').val() == 'in_nolimit') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="im_change">突发重要度变动</option>';
		sort_select += '<option value="acr_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';	    
		time_html += '<input name="time_range" type="radio" value="1"> 过去一天';
		time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 过去七天';
		time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 过去一个月';
		$('#time_choose').append(time_html);
	}
	if($('#range_choose').val() == 'in_limit_domain') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="im_change">突发重要度变动</option>';
		sort_select += '<option value="acr_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';	    
		time_html += '<input name="time_range" type="radio" value="1"> 过去一天';
		time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 过去七天';
		time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 过去一个月';
		$('#time_choose').append(time_html);

		var html = '';
		html += '<select id="range_choose">';
		html += '<option value="">境内机构</option>'
		html += '<option value="">境外机构</option>'
		html += '<option value="">民间组织</option>'
		html += '<option value="">境外媒体</option>'
		html += '<option value="">活跃人士</option>'
		html += '<option value="">商业人士</option>'
		html += '<option value="">媒体人士</option>'
		html += '<option value="">高校</option>'
		html += '<option value="">草根</option>'
		html += '<option value="">媒体</option>'
		html += '<option value="">法律机构及人士</option>'
		html += '<option value="">政府机构及人士</option>'
		html += '<option value="">其他</option>'
		html += '</select>'
	};
	if($('#range_choose').val() == 'in_limit_topic') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="im_change">突发重要度变动</option>';
		sort_select += '<option value="acr_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';	    
		time_html += '<input name="time_range" type="radio" value="1"> 过去一天';
		time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 过去七天';
		time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 过去一个月';
		$('#time_choose').append(time_html);

		var html = '';
		html += '<select id="range_choose">';
		html += '<option value="">科技类</option>';
		html += '<option value="">经济类</option>';
		html += '<option value="">教育类</option>';
		html += '<option value="">军事类</option>';
		html += '<option value="">民生类_健康</option>';
		html += '<option value="">民生类_住房</option>';
		html += '<option value="">民生类_环保</option>';
		html += '<option value="">民生类_就业</option>';
		html += '<option value="">民生类_社会保障</option>';
		html += '<option value="">民生类_交通</option>';
		html += '<option value="">民生类_法律</option>';
		html += '<option value="">政治类_外交</option>';
		html += '<option value="">政治类_暴恐</option>';
		html += '<option value="">政治类_地区和平</option>';
		html += '<option value="">政治类_反腐</option>';
		html += '<option value="">政治类_宗教</option>';
		html += '<option value="">文体类_娱乐</option>';
		html += '<option value="">文体类_体育</option>';
		html += '<option value="">其他类</option>';
		html += '</select>';
	};
	if($('#range_choose').val() == 'in_limit_keyword') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="im_change">突发重要度变动</option>';
		sort_select += '<option value="acr_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';
	    time_html += '<input id="weibo_from" type="text" class="form-control" style="width:145px; display:inline-block;height:25px;">&nbsp;-&nbsp;';
		time_html += '<input id="weibo_to" type="text" class="form-control" style="width:145px; display:inline-block;height:25px">';	    
		$('#time_choose').append(time_html);


		var html = '';
	    html += '<input id="" type="text" class="form-control" style="width:145px;height:25px;" placeholder="请输入关键词">';
	};
	if($('#range_choose').val() == 'in_limit_hashtag') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="im_change">突发重要度变动</option>';
		sort_select += '<option value="acr_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';
	    time_html += '<input id="weibo_from" type="text" class="form-control" style="width:145px; display:inline-block;height:25px;">&nbsp;-&nbsp;';
		time_html += '<input id="weibo_to" type="text" class="form-control" style="width:145px; display:inline-block;height:25px">';	    
		$('#time_choose').append(time_html);


		var html = '';
	    html += '<input id="" type="text" class="form-control" style="width:145px;height:25px;" placeholder="请输入微话题">';
	};
	if($('#range_choose').val() == 'in_limit_geo') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="im_change">突发重要度变动</option>';
		sort_select += '<option value="acr_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';	    
		time_html += '<input name="time_range" type="radio" value="1"> 过去一天';
		time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 过去七天';
		time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 过去一个月';
		$('#time_choose').append(time_html);

		var html = '';
		html += '<select id="range_choose">';
		html += '<option value="北京">北京</option>';
		html += '<option value="天津">天津</option>';
		html += '<option value="上海">上海</option>';
		html += '<option value="重庆">重庆</option>';
		html += '<option value="广东省">广东省</option>';
		html += '<option value="浙江省">浙江省</option>';
		html += '<option value="江苏省">江苏省</option>';
		html += '<option value="福建省">福建省</option>';
		html += '<option value="湖南省">湖南省</option>';
		html += '<option value="湖北省">湖北省</option>';
		html += '<option value="山东省">山东省</option>';
		html += '<option value="辽宁省">辽宁省</option>';
		html += '<option value="吉林省">吉林省</option>';
		html += '<option value="云南省">云南省</option>';
		html += '<option value="四川省">四川省</option>';
		html += '<option value="安徽省">安徽省</option>';
		html += '<option value="江西省">江西省</option>';
		html += '<option value="黑龙江省">黑龙江省</option>';
		html += '<option value="河北省">河北省</option>';
		html += '<option value="陕西省">陕西省</option>';
		html += '<option value="海南省">海南省</option>';
		html += '<option value="河南省">河南省</option>';
		html += '<option value="山西省">山西省</option>';
		html += '<option value="内蒙古">内蒙古</option>';
		html += '<option value="广西">广西</option>';
		html += '<option value="贵州省">贵州省</option>';
		html += '<option value="宁夏">宁夏</option>';
		html += '<option value="青海省">青海省</option>';
		html += '<option value="新疆">新疆</option>';
		html += '<option value="西藏">西藏</option>';
		html += '<option value="甘肃省">甘肃省</option>';
		html += '<option value="台湾省">台湾省</option>';
		html += '<option value="香港">香港</option>';
		html += '<option value="澳门">澳门</option>';
		html += '<option value="国外">国外</option>';
		html += '</select>';
	};
	if($('#range_choose').val() == 'all_nolimit') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="fans">粉丝数</option>';
		sort_select += '<option value="act">发帖数</option>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

	    $('#time_choose').empty();
	    var time_html = '';	    
		time_html += '<input name="time_range" type="radio" value="1"> 过去一天';
		time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 过去七天';
		time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 过去一个月';
		$('#time_choose').append(time_html);

	}
	//全库关键词
	if($('#range_choose').val() == 'all_limit_keyword') {
		var html = '';
	    html += '<input id="" type="text" class="form-control" style="width:145px;height:25px;" placeholder="请输入关键词">';
	    $('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select>';
		sort_select += '<option value="fans">粉丝数</option>';
		sort_select += '<option value="act">发帖数</option>';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';
	    time_html += '<input id="weibo_from" type="text" class="form-control" style="width:145px; display:inline-block;height:25px;">&nbsp;-&nbsp;';
		time_html += '<input id="weibo_to" type="text" class="form-control" style="width:145px; display:inline-block;height:25px">';	    
		$('#time_choose').append(time_html);

		var html = '';
	    html += '<input id="" type="text" class="form-control" style="width:145px;height:25px;" placeholder="请输入关键词">';

	};
	$('#range_choose_detail').append(html);
});

var date = choose_time_for_mode();
date.setHours(0,0,0,0);
var max_date = date.format('yyyy/MM/dd hh:mm');
console.log(max_date);
var current_date = date.format('yyyy/MM/dd hh:mm');
var from_date_time = Math.floor(date.getTime()/1000) - 60*60*24*30;
var min_date_ms = new Date()
min_date_ms.setTime(from_date_time*1000);
var from_date = min_date_ms.format('yyyy/MM/dd hh:mm');
if(global_test_mode==0){
    $('#time_choose #weibo_from').datetimepicker({value:from_date,step:60});
    $('#time_choose #weibo_to').datetimepicker({value:current_date,step:60});
}else{
    $('#time_choose #weibo_from').datetimepicker({value:from_date,step:60,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
    $('#time_choose #weibo_to').datetimepicker({value:current_date,step:60,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
}

//结果分析默认值
$('#rec_range').append($('#range_choose option:selected').text());
$('#rec_detail').append('：');
$('#rec_detail').append($('#range_choose option:selected').text());
$('#rec_rank_by').append($('#sort_select_2 option:selected').text());
var day_select = $("input[name='time_range']:checked").val();
if(day_select == "1"){
	$('#rec_time_range').append('过去一天')
}
if(day_select == "7"){
	$('#rec_time_range').append('过去七天')
}
if(day_select == "30"){
	$('#rec_time_range').append('过去三十天')
}

var data = [['关键词：两会','状态：正在计算'],['关键词：两会','状态：正在计算'],['关键词：两会','状态：正在计算']];
task_status(data);
draw_rank_table(data);