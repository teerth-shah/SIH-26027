import React from 'react';
import { MapContainer, TileLayer, Polyline, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { SECTIONS, STATIONS, DEPARTMENT_COLORS } from '../mockData';

export default function CorridorMap({ selectedBlockId, onSelectBlock, filteredBlocks }) {
  const selectedBlock = filteredBlocks.find((b) => b.id === selectedBlockId);

  return (
    <div style={{ height: '420px', width: '100%', borderRadius: '8px', overflow: 'hidden', border: '1px solid #cbd5e1' }}>
      <MapContainer center={[19.18, 72.97]} zoom={11} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {SECTIONS.map((sec) => (
          <Polyline
            key={sec.id}
            positions={sec.coords}
            pathOptions={{
              color: selectedBlock?.sectionId === sec.id ? '#8b5cf6' : '#64748b',
              weight: selectedBlock?.sectionId === sec.id ? 7 : 4,
              dashArray: selectedBlock?.sectionId === sec.id ? null : '5, 5',
            }}
          >
            <Popup>{sec.name}</Popup>
          </Polyline>
        ))}

        {STATIONS.map((stn) => (
          <CircleMarker
            key={stn.id}
            center={stn.position}
            radius={6}
            pathOptions={{ fillColor: '#ffffff', color: '#0f172a', weight: 2, fillOpacity: 1 }}
          >
            <Popup><strong>Station:</strong> {stn.name}</Popup>
          </CircleMarker>
        ))}

        {filteredBlocks.map((block) => {
          const isSelected = block.id === selectedBlockId;
          return (
            <CircleMarker
              key={block.id}
              center={block.locationCoords}
              radius={isSelected ? 11 : 7}
              pathOptions={{
                fillColor: DEPARTMENT_COLORS[block.department] || '#718096',
                color: isSelected ? '#000000' : '#ffffff',
                weight: isSelected ? 3 : 1,
                fillOpacity: 0.95,
              }}
              eventHandlers={{
                click: () => onSelectBlock(block.id),
              }}
            >
              <Popup>
                <div>
                  <strong>{block.title}</strong> ({block.id})<br />
                  Dept: {block.department}<br />
                  Time: {block.day} {block.startHour}:00 - {block.endHour}:00
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}