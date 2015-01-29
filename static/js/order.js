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
    console.log(post_data);
    var r_data = {};
}
