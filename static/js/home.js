var map = L.map('map').setView([36.719444, -4.420000], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let markers = [];
let devices = [];

function popup_device(device) {
    let div = `<div class="card">
                  <div class="card-body text-center">
                    <h5 class="card-title">`+ device.name +`</h5>
                    <h6 class="card-subtitle mb-2 text-muted">` + device.type +`</h6>
                    <p class="card-text"></p>
                    <a href="/logs_device/` + device["_id"]["$oid"] + `" class="card-link">Más información</a>
                  </div>
                </div>`
    return div
}

(function worker() {
    $.ajax({
        url: '/api/devices/info',
        success: function (data) {
            devices = data.devices;
            markers.forEach(marker => map.removeLayer(marker));
            devices.forEach((device) => {
                let marker = L.marker([device.latitude, device.longitude]).addTo(map);
                marker.bindPopup(popup_device(device))
                markers.push(marker)
            })
        },
        complete: function () {
            setTimeout(worker, 10000); // CADA 10 SEGUNDOS
        }
    });
})();