var engine_test = [
  {
    "name": "Ahmia",
    "url": "http://msydqstlz2kzerdg.onion",
    "status": 200,
    "time": "03/30/2021, 16:45:34"
  },
  {
    "name": "Phobos",
    "url": "http://phobosxilamwcg75xt22id7aywkzol6q6rfl2flipcqoc4e4ahima5id.onion",
    "status": 200,
    "time": "03/30/2021, 16:47:02"
  },
  {
    "name": "Abiko",
    "url": "http://abikogailmonxlzl.onion",
    "status": 200,
    "time": "03/30/2021, 16:47:05"
  },
  {
    "name": "Torch",
    "url": "http://cnkj6nippubgycuj.onion",
    "status": 200,
    "time": "03/30/2021, 16:47:08"
  },
  {
    "name": "Tor66",
    "url": "http://www.tor66sezptuu2nta.onion",
    "status": 200,
    "time": "03/30/2021, 16:47:10"
  },
  {
    "name": "Quo",
    "url": "http://quosl6t6c64mnn7d.onion",
    "status": 200,
    "time": "03/30/2021, 16:47:13"
  },
  {
    "name": "Haystak",
    "url": "http://haystakvxad7wbk5.onion",
    "status": 200,
    "time": "03/30/2021, 16:47:18"
  },
  {
    "name": "OnionSearchEngine",
    "url": "http://5u56fjmxu63xcmbk.onion",
    "status": 200,
    "time": "03/30/2021, 16:47:21"
  }
];
var keyword_test = [
  {
    "keyword": "card",
    "author": "admin",
    "time": "03/30/2021, 17:00:26"
  },
  {
    "keyword": "drug",
    "author": "admin",
    "time": "03/30/2021, 17:00:30"
  },
  {
    "keyword": "fakemoney",
    "author": "admin",
    "time": "03/30/2021, 17:00:37"
  },
  {
    "keyword": "gun",
    "author": "admin",
    "time": "03/30/2021, 17:00:47"
  },
  {
    "keyword": "hack",
    "author": "admin",
    "time": "03/30/2021, 17:00:03"
  }
];
var detect_test = [
  {
    "title": "gun by",
    "url": "http://xjrvaehffrovezeffupq.onion",
    "mirrorUrl": "http://localhost/abcde/test8.html",
    "contentLength": 274,
    "keyword": "gun",
    "status": 200,
    "pk": "00e2dc11b71277c0cb97bc605c149eaa528a33234b5c2f4907606deb64b832a207d9069312039ff95c78fda866e31b2a0209f25d69a78a62f673d62c9178b112",
    "referer": "Ahmia",
    "time": "03/30/2021, 17:12:28"
  },
  {
    "title": "gun by",
    "url": "http://pmduavupfjfojvyfhbhq.onion",
    "mirrorUrl": "http://localhost/abcde/test8.html",
    "contentLength": 334,
    "keyword": "gun",
    "status": 200,
    "pk": "00fa3adae3db2061581fa38509e1533c6151132f785d10c262bc0533395d363dbe05c41ca4210bba20f5e229b19c4bc671acba8377643af9e831776e9979de47",
    "referer": "Ahmia",
    "time": "03/30/2021, 17:12:28"
  },
  {
    "title": "gun by",
    "url": "http://amqkwmpqeoeelxyonvio.onion",
    "mirrorUrl": "http://localhost/abcde/test8.html",
    "contentLength": 112,
    "keyword": "gun",
    "status": 200,
    "pk": "014371552ae6434fd98a421caae285b6ea9daae413ed6c04cae24fea3cccfc959fb689705b662e39d6d1e57a569fc6279bbd44e24b86ca8e3a295d4d215d270c",
    "referer": "Ahmia",
    "time": "03/30/2021, 17:12:28"
  },
  {
    "title": "gun by",
    "url": "http://dsioayqfzhzjpbjqycow.onion",
    "mirrorUrl": "http://localhost/abcde/test8.html",
    "contentLength": 494,
    "keyword": "gun",
    "status": 200,
    "pk": "015c94e4a4f5060486c5d39e158d3134fd06b1a5d6b8ffd7007a15669892034b98767eb5c99ad6df3f461cde6fed6f921d0f874f8010688bdf690baf1feebfcd",
    "referer": "Ahmia",
    "time": "03/30/2021, 17:12:28"
  },
  {
    "title": "gun by",
    "url": "http://wolfkxwyadebrwodrlff.onion",
    "mirrorUrl": "http://localhost/abcde/test8.html",
    "contentLength": 158,
    "keyword": "gun",
    "status": 200,
    "pk": "01bc20320fe7bb504e192065f385ac6a1a4e9147c1071f40e73da1d088945f528080affe8361489f33fc4799f3d1c6e74731d8d0f6e7a509fae5aa83c4be050e",
    "referer": "Ahmia",
    "time": "03/30/2021, 17:12:28"
  }
];

function GetTable(){
  var temp = new Array();
  $.ajax({
      url: 'https://jsonplaceholder.typicode.com/posts?userId=1',
      method: 'get',
      async:false,
      success: function(response) {
        temp = response;
        return temp;
      }
    });
};

tb = {
  SettingList: function() {

        var table_list = engine_test;

        $('tbody#checkEngine').empty();

        function TableSet(response){
          $.each(response, function (index, item){

            // var str = '<tr><td>' + item.name + '</td>';
            // str += '<td>' + '<a href = "' + item.url + '">' + item.url + '</a>' + '</td>';
            // str += '<td>' + item.status + '</td>';
            // str += '<td>' + item.time + '</td>';

            var str = '<tr name="my_list" style="word-break:break-all">';
            for (var n in item){
              if (item[n].length > 4 && item[n].substring(0,4)=='http') {
                 str += '<td>' + '<a href = "' + item[n] + '">' + item[n] + '</a>' + '</td>';
              }
              else {
                  str += '<td>' + item[n] + '</td>';
              }
            }

            str +='<td>';
            str +='<a class="add" title"Add" data-toggle="tooltip" data-placement="top"><i class="material-icons">&#xE03B;</i></a>';
            str +='<a class="edit" title="Edit" data-toggle="tooltip" data-placement="top"><i class="material-icons">&#xE254;</i></a>';
            str +='<a class="delete" title="Delete" data-toggle="tooltip" data-placement="top"><i class="material-icons">&#xE872;</i></a>';
            str +='</td></tr>';

            $('tbody#checkEngine').append(str);
          });
        }

        TableSet(table_list);
  },

  KeywordList: function() {

        var table_list = keyword_test;

        $('tbody#keyword').empty();

        function TableSet(response){
          $.each(response, function (index, item){

            var str = '<tr name="my_list" style="word-break:break-all">';
            for (var n in item){
              str += '<td>' + item[n] + '</td>';
            }

            $('tbody#keyword').append(str);
          });
        }

        TableSet(table_list);
  },

  detectList: function() {

        var table_list = detect_test;
        var temp;
        var mirror = new Array();

        $('tbody#detect').empty();

        function TableSet(response){
          temp = response;

          for (let i = 0; i < temp.length; i ++) {
            delete temp[i].pk;
            mirror[i]=temp[i].mirrorUrl;
            delete temp[i].mirrorUrl;
          }
          $.each(response, function (index, item){

            var str = '<tr name="my_list" style="word-break:break-all">';
            for (var n in item){
              if (item[n].length > 4 && item[n].substring(0,4)=='http') {
                 str += '<td>' + '<a href = "' + mirror[n] + '">' + item[n] + '</a>' + '</td>';
              }
              else {
                  str += '<td>' + item[n] + '</td>';
              }
            }

            $('tbody#detect').append(str);
          });
        }

        TableSet(table_list);
  }
};
