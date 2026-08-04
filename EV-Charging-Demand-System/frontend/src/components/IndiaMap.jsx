import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import InfoCard from "./InfoCard";

const getIcon = (level) =>
  new L.Icon({
    iconUrl:
      level === "High"
        ? "https://maps.google.com/mapfiles/ms/icons/red-dot.png"
        : level === "Medium"
          ? "https://maps.google.com/mapfiles/ms/icons/orange-dot.png"
          : "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
  });

export default function IndiaMap({ predictions }) {
  const [selectedCity, setSelectedCity] = useState(null);

  return (
    <section className="panel-surface map-panel">
      <div className="panel-heading">
        <p className="eyebrow">Geographic View</p>
        <h2>City Demand Map</h2>
        <p className="section-copy">
          Explore predicted charging demand across cities and inspect each
          location for deployment signals.
        </p>
      </div>

      <div className="map-frame">
        <MapContainer
          center={[22.5937, 78.9629]}
          zoom={5}
          minZoom={4}
          style={{ height: "100%", width: "100%" }}
          maxBounds={[
            [6, 68],
            [37, 98],
          ]}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="(c) OpenStreetMap contributors"
          />

          {Array.isArray(predictions) &&
            predictions.map((city) =>
              city.latitude && city.longitude ? (
                <Marker
                  key={city.city}
                  position={[Number(city.latitude), Number(city.longitude)]}
                  icon={getIcon(city.demand_level || city.level)}
                  eventHandlers={{
                    click: () => setSelectedCity(city),
                  }}
                >
                  <Popup>
                    <b>{city.city}</b>
                    <br />
                    Demand: <b>{city.demand_level || city.level}</b>
                    <br />
                    Score: {city.score}
                  </Popup>
                </Marker>
              ) : null
            )}
        </MapContainer>
      </div>

      {selectedCity ? (
        <InfoCard data={selectedCity} />
      ) : (
        <div className="info-card muted-card">
          <h3>Select a city marker</h3>
          <p>Demand details will appear here after you tap a location on the map.</p>
        </div>
      )}
    </section>
  );
}
