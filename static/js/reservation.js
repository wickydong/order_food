// add user phone and user_name into input
$(document).ready(function(){
    if (postData['user_name'] != null) {
        $('#userName').val(postData['user_name']);
    }
    if (postData['phone_number'] != null) {
        $('#phoneNumber').val(postData['phone_number']);
    }
});
// change postData['come_date']
//var datef = new Date();

$(".date").on("click", function(event) {
    var index = $(".date").index(this);
    var date = new Date();
    date.setDate(date.getDate() + index);
    postData.come_date = date.toISOString().slice(0,10);
});

/*$("#come_data_1").click(function(){
    postData['come_date']   = datef.getFullYear()+'-'+(datef.getMonth()+1)+'-'+datef.getDate();
    $(this).css('background','red');
    $("#come_data_2").css('background','#fff');
    $("#come_data_3").css('background','#fff');
});
$("#come_data_2").click(function(){
    postData['come_date']   = datef.getFullYear()+'-'+(datef.getMonth()+1)+'-'+(datef.getDate()+1);
    $(this).css('background','red');
    $("#come_data_1").css('background','#fff');
    $("#come_data_3").css('background','#fff');
});
$("#come_data_3").click(function(){
    postData['come_date']   = datef.getFullYear()+'-'+(datef.getMonth()+1)+'-'+(datef.getDate()+2);
    $(this).css('background','red');
    $("#come_data_1").css('background','#fff');
    $("#come_data_2").css('background','#fff');
});*/
// change postData['come_time']
var hour = null;
var minute = null;
$("#come_time_hour").change(function(){
    hour = $(this).val();
    if (hour && minute) {
        postData['come_time'] = hour + ':'+minute+':00';
        console.log(postData['come_time']);
    }
});
$("#come_time_minute").change(function(){
    minute = $(this).val();
    if (hour && minute) {
        postData['come_time'] = hour + ':'+minute+':00';
        console.log(postData['come_time']);
    }
});
/*
// change postData['user_name']
$("#userName").change(function(){
    postData['user_name'] = $(this).val()
});
// change postData['phone']
$("#phoneNumber").change(function(){
    postData['phone_number'] = $(this).val()
});
// change postData['come_people']
$("#comePeople").change(function(){
    postData['come_people'] = $(this).val();
});
// change postData['room_type']
$("#roomType").change(function(){
    postData['room_type'] = $(this).val();
});
$("#otherContent").change(function(){
    postData['other'] = $(this).val();
});
*/
// submit form
$("#submit_btn").click(function(){
    // get data
    postData['user_name'] = $("#user_name").val();
    postData['phone_number'] = $("#phone_number").val();
    postData['come_people'] = $("#come_people").val();
    postData['room_type'] = $("#room_type").val();
    postData['other'] = $("#otherContent").val();

    var r_varify = varifty(postData);
    var errorList = ['user_name', 'phone_number', 'come_people', 'room_type'];
    if (r_varify['status'] == 'error') {
        console.log(r_varify['string']);
        //if (r_varify['dome_id']) {
        if(r_varify['dome_id'] in errorList)
            $("#"+r_varify['dome_id']).parent().addClass("ui-error");//css('border', '1px solid #f00');
        } else {
            alert(r_varify['string']);
        }
    } else if (r_varify['status'] == 'success') {
        $.post(
            '/reservation',
            postData,
            function(data){
                if (data=="ok"){
                               window.location.href="http://baidu.com";
                               }
            }
        );
    }
});
var varifty = function(post_data){
    console.log(post_data);
    var list = [
            'open_id',
            'user_status',
            'user_name',
            'phone_number',
            'come_date',
            'come_time',
            'come_people',
            'room_type'
        ];
    var r_data = {};

    for(var i in list) {
        if(!post_data[list[i]]) {
            r_data['status'] = "error";
            r_data['string'] = list[i] + "is empty";
            r_data["dome_id"] = list[i];
            return r_data;
        }
    }

    /*if (!post_data['open_id']) {
        r_data['status'] = 'error';
        r_data['string'] = 'open_id is null';
        r_data['dome_id'] = '';
        return r_data;
    } else if (!post_data['user_status']) {
        r_data['status'] = 'error';
        r_data['string'] = 'user_status is null';
        r_data['dome_id'] = '';
        return r_data;
    } else if (!post_data['user_name']) {
        r_data['status'] = 'error';
        r_data['string'] = 'user_name is null';
        r_data['dome_id'] = '#userName';
        return r_data;
    } else if (!post_data['phone_number']) {
        r_data['status'] = 'error';
        r_data['string'] = 'phone number is null';
        r_data['dome_id'] = 'phoneNumber';
        return r_data;
    } else if (!post_data['come_date']) {
        r_data['status'] = 'error';
        r_data['string'] = 'come_date is null';
        r_data['dome_id'] = '';
        return r_data;
    } else if (!post_data['come_time']) {
        r_data['status'] = 'error';
        r_data['string'] = 'come_time is null';
        r_data['dome_id'] = '';
        return r_data;
    } else if (!post_data['come_people']) {
        r_data['status'] = 'error';
        r_data['string'] = 'come_people is null';
        r_data['dome_id'] = '#comePeople';
        return r_data;
    } else if (!post_data['room_type']) {
        r_data['status'] = 'error';
        r_data['string'] = 'room_type is null';
        r_data['dome_id'] = '#roomType';
        return r_data;
    } else{
        if (!post_data['other']) {
            post_data['other'] = null;
        }
        r_data['status'] = 'success';
        return r_data;
    }*/
}
