// add user phone and user_name into input
$(document).ready(function(){
    if (postData['user_name'] != null) {
        $('#user_name').val(postData['user_name']);
    }
    if (postData['phone_number'] != null) {
        $('#phone_number').val(postData['phone_number']);
    }
    $("input").focus(function(){
        $(this).removeClass("error-input");
	$(this).parent().removeClass("ui-error");
    });
});
// change postData['come_date']
//var datef = new Date();

$(".date").on("click", function(event) {
    var index = $(".date").index(this);
    var date = new Date();
    date.setDate(date.getDate() + index);
    postData.come_date = date.toISOString().slice(0,10);
});
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
// submit form
$("#submit_btn").click(function(){
    // get data
    postData['user_name'] = $("#user_name").val();
    postData['phone_number'] = $("#phone_number").val();
    postData['come_people'] = $("#come_people").val();
    postData['other'] = $("#otherContent").val();

    var r_varify = varifty(postData);
    var errorList = ['user_name', 'phone_number', 'come_people'];
    if (r_varify['status'] == 'error') {
        console.log(r_varify['string']);
	console.log(r_varify['dome_id']);
        //if (r_varify['dome_id']) {
        if($.inArray(r_varify['dome_id'], errorList) >= 0) {
            $("#"+r_varify['dome_id']).parent().addClass("ui-error");//css('border', '1px solid #f00');
        } else {
            alert(r_varify['string']);
        }
    } else if (r_varify['status'] == 'success') {
        $.post(
            '/reservation',
            postData,
            function(data){
                if (data != "wrong"){
                    window.location.href="/reservation_sure/"+data;
                }
            }
        );
    }
});
var varifty = function(post_data){
    console.log(post_data);
    var list = [
            'base_64',
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
            r_data['string'] = list[i] + " is empty";
            r_data["dome_id"] = list[i];
            return r_data;
        }
    }
    r_data['status'] = 'success';
    return r_data;
}
