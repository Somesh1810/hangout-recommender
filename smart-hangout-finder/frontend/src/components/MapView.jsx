import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView({ places }) {
  const center =
    places.length > 0
      ? [places[0].lat, places[0].lon]
      : [12.9716, 77.5946];

  return (
    <MapContainer
      center={center}
      zoom={13}
      style={{
        height: "500px",
        width: "100%",
        borderRadius: "16px",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {places.map((place, index) => (
        <Marker
          key={index}
          position={[place.lat, place.lon]}
        >
          <Popup>
            <strong>{place.name}</strong>
            <br />
            {place.type}
            <br />
            Distance: {place.distance_km} km
            <br />
            Budget: ₹{place.budget}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}