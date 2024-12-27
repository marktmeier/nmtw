document.addEventListener('DOMContentLoaded', function() {
    const locationStatus = document.getElementById('location-status');
    const submitBtn = document.getElementById('submit-btn');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');

    function handleLocationSuccess(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        
        latitudeInput.value = latitude;
        longitudeInput.value = longitude;
        
        locationStatus.className = 'alert alert-success';
        locationStatus.innerHTML = '<i class="bi bi-check-circle"></i> Location detected successfully';
        
        submitBtn.disabled = false;
    }

    function handleLocationError(error) {
        locationStatus.className = 'alert alert-danger';
        locationStatus.innerHTML = `
            <i class="bi bi-exclamation-triangle"></i>
            Unable to detect location. Please enable location services and refresh the page.
            <br>
            Error: ${error.message}
        `;
    }

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(handleLocationSuccess, handleLocationError, {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        });
    } else {
        locationStatus.className = 'alert alert-danger';
        locationStatus.innerHTML = '<i class="bi bi-exclamation-triangle"></i> Geolocation is not supported by your browser';
    }
});
