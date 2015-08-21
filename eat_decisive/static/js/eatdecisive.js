$(document).ready(function() {
      $("#decideNow").click(function(event) {
        event.preventDefault();
        if ($("#food").val()=="") {
            $("#success").hide();
            $("#fail").fadeIn();
        } else {                
          //var food = $("#food").val();
//          var foodList = $("#food").val().split("*");
//          var numItems = foodList.length;
//          var randomIndex = Math.floor(Math.random() * numItems);
//          var decision = foodList[randomIndex];
//          var dataString = 'food='+food;
            var food;
            food = $('#food').val();
            function(data) {
              $(".landingpage").hide();
              $("#fail").hide();
              $("#success").html(data);
              $("#success").show();
              $("#return").show();
            }
        }
      });
});


