type = ['primary', 'info', 'success', 'warning', 'danger'];
var list_data;
var url_list;

function PostList(dict) {
  $.ajax({
      url: '',
      method: 'post',
      data: dict,
      async:true,
      success: function(data) {
        console.log("success");
      },
      error: function(error) {
        alert("post error");
      }
  });
}
//사용자 세팅 최신화하기
function UpdateList(lkey, lvalue){
  var list_index = new Object();
  for (var i in lkey){
    list_index[lkey[i]] = lvalue[i];
  };

  for (i in url_list) {
    if(url_list[i].url == list_index.url){
      url_list[i] = list_index;
      PostList(url_list);
      break;
    }
  }
  url_list[Number(i)+1] = list_index;
  PostList(url_list);
}

demo = {
  AddData: function() {

    // 인풋에서 데이터 읽어오기
    function ReadInput() {
      var temp = new Array();
      $('input[name="input-data"]').each(function(index, item){
        // console.log(index);
        // console.log(item);
        temp.push($(item).val());
      });
      return temp;
    };

    $('[data-toggle="tooltip"]').tooltip({
      trigger : 'hover'
    });
    var actions = '<a class="add" title="Add" data-toggle="tooltip" data-placement="top"><i class="material-icons" id="add">&#xE03B;</i></a>' +
      '<a class="edit" title="Edit" data-toggle="tooltip" data-placement="top"><i class="material-icons" id="edit">&#xE254;</i></a>' +
      '<a class="delete" title="Delete" data-toggle="tooltip" data-placement="top"><i class="material-icons">&#xE872;</i></a>';

    // Append table with add row form on add new button click
    $(".add-new").click(function(){
      $(this).attr("disabled", "disabled");
      var index = $("table tbody tr:last-child").index();

      var row = '<tr>' +
          '<td><input type="text" class="form-control" name="input-data"></td>' +
          '<td><input type="text" class="form-control" name="input-data"></td>' +
          '<td><input type="text" class="form-control" name="input-data"></td>' +
          '<td><input type="text" class="form-control" name="input-data"></td>' +
          '<td>' + actions + '</td>' +
          '</tr>';
      $("table").append(row);
      // toggle()이 현재 속성 반대로 해준다 함.(hide/show)  현재(add:hide/edit:show) -> 과거(add:show/edit:hide)
      $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
      console.log(index + 1);
      console.log($("table tbody tr").eq(index + 1));
      console.log($("table tbody tr").eq(index + 1).find(".add, .edit"));

      $('[data-toggle="tooltip"]').tooltip({trigger : 'hover'});
    });
    // Add row on add button click

    $(document).on("click", ".add", function(){
        $('[data-toggle="tooltip"]').tooltip('hide');
        var empty = false;
        var input = $(this).parents("tr").find('input[type="text"]');

        var new_list = new Array();
        new_list = ReadInput();
        console.log(new_list);


        input.each(function(){
          if(!$(this).val()){
            $(this).addClass("error");
            empty = true;
          }
          else{
            $(this).removeClass("error");
          }
      });

      $(this).parents("tr").find(".error").first().focus();
      if(!empty){
        input.each(function(){
          $(this).parent("td").html($(this).val());
        });
        $(this).parents("tr").find(".add, .edit").toggle();
        $(".add-new").removeAttr("disabled");
      }
    });
    // Edit row on edit button click
    $(document).on("click", ".edit", function(){
      $('[data-toggle="tooltip"]').tooltip('hide');
      $(this).parents("tr").find("td:not(:last-child)").each(function(){
        $(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
      });
      $(this).parents("tr").find(".add, .edit").toggle();
      $(".add-new").attr("disabled", "disabled");
    });
    // Delete row on delete button click
    $(document).on("click", ".delete", function(){
      $('[data-toggle="tooltip"]').tooltip('hide');
      $(this).parents("tr").remove();
      $(".add-new").removeAttr("disabled");
    });
  },


  initPickColor: function() {
    $('.pick-class-label').click(function() {
      var new_class = $(this).attr('new-class');
      var old_class = $('#display-buttons').attr('data-class');
      var display_div = $('#display-buttons');
      if (display_div.length) {
        var display_buttons = display_div.find('.btn');
        display_buttons.removeClass(old_class);
        display_buttons.addClass(new_class);
        display_div.attr('data-class', new_class);
      }
    });
  },

  //notification
  showNotification: function(from, align) {
    color = Math.floor((Math.random() * 4) + 1);

    $.notify({
      icon: "tim-icons icon-bell-55",
      message: "Welcome to <b>Black Dashboard</b> - a beautiful freebie for every web developer."

    }, {
      type: type[color],
      timer: 8000,
      placement: {
        from: from,
        align: align
      }
    });
  },

//없어도 현재 구현한건 잘 돌아감
  initDocChart: function() {
    chartColor = "#FFFFFF";

    // General configuration for the charts with Line gradientStroke
    gradientChartOptionsConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        bodySpacing: 4,
        mode: "nearest",
        intersect: 0,
        position: "nearest",
        xPadding: 10,
        yPadding: 10,
        caretPadding: 10
      },
      responsive: true,
      scales: {
        yAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }],
        xAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }]
      },
      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 15,
          bottom: 15
        }
      }
    };

    ctx = document.getElementById('lineChartExample').getContext("2d");

    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, '#80b6f4');
    gradientStroke.addColorStop(1, chartColor);

    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

    myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Active Users",
          borderColor: "#f96332",
          pointBorderColor: "#FFF",
          pointBackgroundColor: "#f96332",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 1,
          pointRadius: 4,
          fill: true,
          backgroundColor: gradientFill,
          borderWidth: 2,
          data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
        }]
      },
      options: gradientChartOptionsConfiguration
    });
  }
};
