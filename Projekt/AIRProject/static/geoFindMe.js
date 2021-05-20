function geoFindMe() {
const latitudeel = document.getElementById("latitude");
const longitudeel = document.getElementById("longitude");


function success(position) {
  const latitude  = position.coords.latitude;
  const longitude = position.coords.longitude;


  latitudeel.value=`${latitude}`
  longitudeel.value=`${longitude}`
}

function error() {

}

if(!navigator.geolocation) {
  
} else {

  navigator.geolocation.getCurrentPosition(success, error);
}

}
geoFindMe();