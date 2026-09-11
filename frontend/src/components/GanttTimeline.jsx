import React from 'react';
import { SECTIONS, DEPARTMENT_COLORS } from '../mockData';

const HOURS = Array.from({ length: 24 }, (_, i) => i);

export default function GanttTimeline({ selectedBlockId, onSelectBlock, filteredBlocks = [], conflicts = [] }) {
  // Extract block IDs involved in conflicts
  const conflictingBlockIds = new Set(
    conflicts.flatMap((c) => [c.blockA?.id, c.blockB?.id]).filter(Boolean)
  );

  return (
    /* 
       THE FIX: 
       1. Changed overflowX to overflow: 'auto' (enables BOTH vertical and horizontal scrollbars).
       2. Added height: '100%' so it takes up the exact box space App.jsx gives it.
       3. Removed the hardcoded border so it blends perfectly with your new UI.
    */
    <div style={{ overflow: 'auto', height: '100%', width: '100%', padding: '16px', background: '#fff', boxSizing: 'border-box' }}>
      
      {/* Header & Legend Area */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', minWidth: '850px' }}>
        <h3 style={{ margin: 0, color: '#1e293b', fontWeight: 'bold', fontSize: '16px' }}>Maintenance Timeline</h3>
        
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          {Object.entries(DEPARTMENT_COLORS).map(([dept, color]) => (
            <div key={dept} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px' }}>
              <span style={{ width: '12px', height: '12px', background: color, borderRadius: '2px', display: 'inline-block' }} />
              {dept}
            </div>
          ))}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: '#dc2626', fontWeight: 'bold' }}>
            <span style={{ width: '12px', height: '12px', border: '2px solid #dc2626', background: '#fee2e2', borderRadius: '2px', display: 'inline-block' }} />
            Conflict
          </div>
        </div>
      </div>

      {/* The Scrollable Grid */}
      <div style={{ minWidth: '850px' }}>
        
        {/* Time Headers */}
        <div style={{ display: 'grid', gridTemplateColumns: '160px repeat(24, 1fr)', borderBottom: '2px solid #cbd5e0' }}>
          <div style={{ fontWeight: 'bold', padding: '8px', fontSize: '12px', color: '#475569' }}>Section / Time</div>
          {HOURS.map((h) => (
            <div key={h} style={{ textAlign: 'center', fontSize: '10px', padding: '4px 0', borderLeft: '1px solid #edf2f7', color: '#64748b' }}>
              {h.toString().padStart(2, '0')}:00
            </div>
          ))}
        </div>

        {/* Section Rows */}
        {SECTIONS.map((sec) => (
          <div key={sec.id} style={{ display: 'grid', gridTemplateColumns: '160px repeat(24, 1fr)', borderBottom: '1px solid #e2e8f0', position: 'relative', minHeight: '52px' }}>
            <div style={{ fontWeight: '600', padding: '12px 8px', fontSize: '12px', background: '#f8fafc', borderRight: '1px solid #e2e8f0', color: '#1e293b' }}>
              {sec.name}
            </div>

            {HOURS.map((h) => (
              <div key={h} style={{ borderLeft: '1px solid #f1f5f9', height: '100%' }} />
            ))}

            {filteredBlocks.filter((b) => b.sectionId === sec.id).map((block) => {
              const startCol = block.startHour + 2;
              const duration = block.endHour - block.startHour;
              const isSelected = block.id === selectedBlockId;
              const hasConflict = conflictingBlockIds.has(block.id);

              return (
                <div
                  key={block.id}
                  onClick={() => onSelectBlock(block.id)}
                  style={{
                    gridColumn: `${startCol} / span ${duration}`,
                    background: hasConflict ? '#ef4444' : (DEPARTMENT_COLORS[block.department] || '#718096'),
                    color: '#fff',
                    borderRadius: '4px',
                    margin: '6px 2px',
                    padding: '6px 8px',
                    fontSize: '11px',
                    cursor: 'pointer',
                    overflow: 'hidden',
                    whiteSpace: 'nowrap',
                    textOverflow: 'ellipsis',
                    border: hasConflict ? '2px solid #991b1b' : 'none',
                    outline: isSelected ? '3px solid #0f172a' : 'none',
                    boxShadow: isSelected ? '0 0 8px rgba(0,0,0,0.4)' : 'none',
                    zIndex: isSelected ? 3 : (hasConflict ? 2 : 1),
                  }}
                  title={`${block.title} (${block.department}): ${block.startHour}:00 - ${block.endHour}:00 ${hasConflict ? '[CONFLICT DETECTED]' : ''}`}
                >
                  <strong>{hasConflict ? '⚠️ ' : ''}{block.id}:</strong> {block.title}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}