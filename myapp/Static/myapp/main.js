
function Switch(obj, index){
  var career = document.getElementsByClassName('careerStats');
  var current = document.getElementsByClassName('currentStats');
  var el = obj.getAttribute('class');

  if (el === 'career'){
    current[index].classList.add('hidden');
    career[index].classList.remove('hidden');
    obj.classList.add('active');
    var c = document.getElementsByClassName('season');
    c[index].classList.remove('active');
    console.log(c[index]);
  }
  else if (el === 'season') {
    career[index].classList.add('hidden');
    current[index].classList.remove('hidden');
    obj.classList.add('active');
    var d = document.getElementsByClassName('career');
    d[index].classList.remove('active');
    console.log(d[index]);
  }
}



function yearlyStats(obj, index){
  p1_year = document.getElementsByClassName('dropdown-years')
  el = obj.getAttribute('class')
  if (el == 'dropbtn'){
    p1_year[index].classList.toggle("hidden");
  }

}


function advancePlayerId(name){
  var request = new XMLHttpRequest()

  // Open a new connection, using the GET request on the URL endpoint
  body = request.open('GET', `https://www.balldontlie.io/api/v1/players?search=${name}`, false)
  request.onload = function () {
    // Begin accessing JSON data here
    var data = JSON.parse(this.response)
    id = data["data"][0]["id"]

    if (request.status >= 200 && request.status < 400) {
      // console.log(id)
    } else {
      console.log('error')
    }
  }
  // console.log(id)
  request.send()
  return id
}



function advanceStats(name, year, index){
  var id = advancePlayerId(name);
  var request = new XMLHttpRequest();

  // Open a new connection, using the GET request on the URL endpoint
  body = request.open('GET', `https://www.balldontlie.io/api/v1/season_averages?season=${year}&player_ids[]=${id}`, false)
  request.onload = function () {
    // Begin accessing JSON data here
    var data = JSON.parse(this.response);

    if (request.status >= 200 && request.status < 400){
      console.log(data["data"].length)
      var pts = data["data"][0]["pts"];
      pts_el = document.getElementsByClassName('p1-pts');
      pts_el[index].innerHTML = "Points: "+ pts;
      var reb = data["data"][0]["reb"];
      reb_el = document.getElementsByClassName('p1-reb');
      reb_el[index].innerHTML = "Rebounds: " + reb;
      var ast = data["data"][0]["ast"];
      ast_el = document.getElementsByClassName('p1-ast');
      ast_el[index].innerHTML = "Assists: " + ast;
      var stl = data["data"][0]["stl"];
      stl_el = document.getElementsByClassName('p1-stl');
      stl_el[index].innerHTML = "Steels: " + stl;
    } else {
      var c = document.getElementsByClassName("p1-advance").childNodes;
      for (i=0;i< c.length; i++){
        c[i].innerHTML = ""
      }

      console.log('error');
    }
  }

  request.send();
}

// console.log(test_id)
// advanceStats(test_id, 2014);















// function test(){
//   arr = [7,2,5,6,9,2]
//
//   new_arr = []
//
//   for(i=0; i< arr.length; i++){
//     if (arr[i] % 2 !== 0){
//       console.log('index:'+ i)
//       console.log('number:'+ arr[i])
//       new_arr.push(arr[i])
//     }
//   }
//
// return new_arr
// }
