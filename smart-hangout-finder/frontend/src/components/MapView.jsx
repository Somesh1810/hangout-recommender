import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

import "leaflet/dist/leaflet.css";

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default function MapView({ places }) {
  if (!places.length) return null;

  return (
    <MapContainer
      center={[places[0].lat, places[0].lon]}
      zoom={13}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {places.map((place, index) => (
        <Marker
          key={index}
          position={[place.lat, place.lon]}
        >
          <Popup>
            <b>{place.name}</b>
            <br />
            {place.cuisine}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}