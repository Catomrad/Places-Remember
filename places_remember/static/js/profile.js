document.addEventListener("DOMContentLoaded", function() {
    ymaps.ready(init);

    function init() {
        var mapElement = document.getElementById('map');
        var coordinatesData = mapElement.getAttribute('data-coordinates');

        try {
            var coordinates = JSON.parse(coordinatesData);
        } catch (e) {
            console.error("Error parsing JSON: ", e);
            return;
        }

        console.log("Parsed coordinates: ", coordinates);

        var map = new ymaps.Map(mapElement, {
            center: [55.992177, 92.795343], // Замените на нужные координаты для центра карты
            zoom: 5
        });

        coordinates.forEach(function(coord) {
            var placemark = new ymaps.Placemark(coord.coords, {
                hintContent: coord.title,
                balloonContent: coord.description
            });
            map.geoObjects.add(placemark);
        });
    }
});