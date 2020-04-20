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
