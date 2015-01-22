// add user phone and user_name into input
$(document).ready(function(){
    if (postData['phone'] != null) {
        $('#userName').val(postData['phone']);
    }
    if (postData['user_name'] != null) {
        $('#phoneNumber').val(postData['user_name']);
    }
});
// change postData['come_date']
var datef = new Date();
$("#come_data_1").click(function(){
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
});
// submit form
$("#submit_btn").click(function(){
    var r_varify = varifty(postData);
    if (r_varify['status'] == 'error') {
        console.log(r_varify['string']);
        if (r_varify['dome_id']) {
            $(r_varify['dome_id']).css('border', '1px solid #f00');
        } else {
            alert(r_varify['string']);
        }
    } else if (r_varify['status'] == 'success') {
        postData['other'] = $('#otherContent').val();
        $.post(
            '/reservation',
            postData,
            function(data){
                console.log(data);
            }
        );
    }
});
var varifty = function(post_data){
    var r_data = {};
    if (!post_data['open_id']) {
        r_data['status'] = 'error';
        r_data['string'] = 'open_id is null';
        r_data['dome_id'] = '';
        return r_data;
    }
    if (!post_data['user_status']) {
        r_data['status'] = 'error';
        r_data['string'] = 'user_status is null';
        r_data['dome_id'] = '';
        return r_data;
    }
    if (!post_data['user_name']) {
        r_data['status'] = 'error';
        r_data['string'] = 'user_name is null';
        r_data['dome_id'] = '#userName';
        return r_data;
    }
    if (!post_data['phone']) {
        r_data['status'] = 'error';
        r_data['string'] = 'phone is null';
        r_data['dome_id'] = 'phoneNumber';
        return r_data;
    }
    if (!post_data['come_date']) {
        r_data['status'] = 'error';
        r_data['string'] = 'come_date is null';
        r_data['dome_id'] = '';
        return r_data;
    }
    if (!post_data['come_time']) {
        r_data['status'] = 'error';
        r_data['string'] = 'come_time is null';
        r_data['dome_id'] = '';
        return r_data;
    }
    if (!post_data['come_people']) {
        r_data['status'] = 'error';
        r_data['string'] = 'come_people is null';
        r_data['dome_id'] = '#comePeople';
        return r_data;
    }
    if (!post_data['room_type']) {
        r_data['status'] = 'error';
        r_data['string'] = 'room_type is null';
        r_data['dome_id'] = 'roomType';
        return r_data;
    }
}
