var map = L.map('map').setView([36.719444, -4.420000], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let markers = [];
let devices = [];

function format_datetime(date) {
    return new Date(date).toLocaleString();
}

function popup_device(device) {
    let last_log_action = "";
    let last_log_date = "";
    if (device.last_log) {
        last_log_action = device.last_log.action;
        last_log_date = format_datetime(device.last_log.date["$date"]);
    }
    let last_heartbeat_action = "";
    let last_heartbeat_date = "";
    if (device.last_heartbeat) {
        last_heartbeat_action = device.last_heartbeat.action;
        last_heartbeat_date = format_datetime(device.last_heartbeat.date["$date"]);
    }
    let div = `<div class="card" style="background-color">
                  <div class="card-body text-center">
                    <h5 class="card-title">` + device.name + `</h5>
                    <h6 class="card-subtitle mb-2 text-muted">` + device.type + `</h6>
                    <p class="card-text">
                        <span><b>Last Heartbeat: </b>` + last_heartbeat_action + `(` + last_heartbeat_date + `)</span><br/>
                        <span><b>Last Log: </b>` + last_log_action + `(` + last_log_date + `)</span><br/>
                    </p>
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
                let color_marker = "red";
                if (device.last_heartbeat && device.last_heartbeat.success) {
                    color_marker = "green";
                }
                var icon_marker = new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-' + color_marker + '.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                });
                let marker = L.marker([device.latitude, device.longitude], {icon: icon_marker}).addTo(map);
                marker.bindPopup(popup_device(device))
                markers.push(marker)
            })
        },
        complete: function () {
            setTimeout(worker, 10000); // CADA 10 SEGUNDOS
        }
    });
})();