function getCurrentLocation() {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            console.log(pos);
            lat = pos['lat'];
            lng = pos['lng'];
            window.location.href = '/nearby-places?lat='+lat+'&lng='+lng;
        });
    }
}
