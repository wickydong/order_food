// submit form
$(document).ready(function(){
  foodMoney = new Array();
  $.getJSON(
  "/getfood",
  function(data){
    for (x in data) {
      var tempHtml = '<li id="'+x+'"><div class="list-img"><img src="'+data[x][0]+'"/></div>';
      tempHtml += '<div class="list-foodname"><p class="food-name">'+data[x][1]+'</p><p class="food-money"><strong>￥</strong><span><span></p></div>';
      tempHtml += '<div class="list-btn"><a href="javascript:;" class="sub-food-num">-</a>';
      tempHtml += '<a href="javascript:;" class="sum-food-num">0</a>';
      tempHtml += '<a href="javascript:;" class="add-food-num">+</a></div></li>';
      $("ul.food-list").append(tempHtml);
      foodMoney[x] = [0,data[x][1],data[x][2]];
    }
    $("div.list-foodname").click(add_one_food);
    $("div.list-img").click(add_one_food);
    $(".add-food-num").click(function(){
      food_num_dom = $(this).parent("div").children(".sum-food-num");
      var food_num = Number(food_num_dom.html());
      var food_id  = $(this).parents("li").attr("id");
      if (food_num == 0) {
        food_num_dom.html(1);
        food_num_dom.show();
        $(this).parent("div").children(".sub-food-num").show();
        $(this).parents("li").find(".food-money").show();
        $(this).parents("li").find(".food-money").children("span").html(sum_food_money(1, foodMoney[food_id][2]));
        foodMoney[food_id][0] = 1;
      } else if (food_num >= 1) {
        food_num_dom.show();
        $(this).parent("div").children(".sub-food-num").show();
        food_num += 1;
        food_num_dom.html(food_num);
        food_num_dom.show();
        $(this).parent("div").children(".sub-food-num").show();
        $(this).parents("li").find(".food-money").show();
        $(this).parents("li").find(".food-money").children("span").html(sum_food_money(food_num, foodMoney[food_id][2]));
        foodMoney[food_id][0] = food_num;
      }
      console.log(food_num);
    });
    $(".sub-food-num").click(function(){
      food_num_dom = $(this).parent("div").children(".sum-food-num");
      var food_num = Number(food_num_dom.html());
      var food_id  = $(this).parents("li").attr("id");
      if (food_num == 1) {
        $(this).hide();
        food_num_dom.html("");
        food_num_dom.hide();
        $(this).parents("li").find(".food-money").hide();
        $(this).parents("li").find(".food-money").children("span").html("");
        foodMoney[food_id][0] = 0;
      } else if (food_num >= 2) {
        food_num -= 1;
        food_num_dom.html(food_num);
        $(this).parents("li").find(".food-money").show();
        $(this).parents("li").find(".food-money").children("span").html(sum_food_money(food_num, foodMoney[food_id][2]));
        foodMoney[food_id][0] = food_num;
      }
      console.log(food_num);
    });
  }
  );
});
$("#submit_btn").click(function(){
    console.log(foodMoney);
    var postFood = new Array();
    for (x in foodMoney) {
      if (foodMoney[x][0] != 0) {
        postFood.push(foodMoney[x]);
      }
    }
    if (c_from == 'order') {
      $.post(
        "/order_food",
        {'dishes':JSON.stringify(postFood),'open_id':open_id},
        function(data){
          window.location.href='／takeout_html/'+data;
        }
      );
    }
    if (c_from == 'takeout') {
      $.post(
          "/takeout",
          {'dishes':JSON.stringify(postFood),'open_id':open_id},
          function(data){
            window.location.href='/reservation/'+data;
          }
        );
    }
});
var varifty = function(post_data){
    console.log(post_data);
    var r_data = {};
}

// change food num
var sum_food_money = function(num, money){
  console.log((Number(num)*Number(money)).toFixed(2));
  return (Number(num)*Number(money)).toFixed(2);
}
var add_one_food = function(){
  var food_num_dom = $(this).parent("li").find(".sum-food-num");
  var food_num = Number(food_num_dom.html());
  var food_id  = $(this).parent("li").attr("id");
  foodMoney[food_id][0] = 1;
  if (food_num == 0) {
    food_num_dom.html(1);
    food_num_dom.show();
    $(this).parent("li").find(".sub-food-num").show();
    $(this).parent("li").find(".food-money").show();
    $(this).parent("li").find(".food-money").children("span").html(sum_food_money(1, foodMoney[food_id][2]));
  }
}
