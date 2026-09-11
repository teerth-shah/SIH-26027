/**
 * Analyzes maintenance blocks for overlapping time slots on the same corridor section.
 * @param {Array} blocks 
 * @returns {Array} List of detected conflicts with conflicting block IDs and details.
 */
export function detectScheduleConflicts(blocks) {
  const conflicts = [];

  for (let i = 0; i < blocks.length; i++) {
    for (let j = i + 1; j < blocks.length; j++) {
      const blockA = blocks[i];
      const blockB = blocks[j];

      // Check if blocks share the same section and day
      if (blockA.sectionId === blockB.sectionId && blockA.day === blockB.day) {
        // Check for time range overlap: (StartA < EndB) AND (EndA > StartB)
        const timeOverlap = blockA.startHour < blockB.endHour && blockA.endHour > blockB.startHour;

        if (timeOverlap) {
          conflicts.push({
            id: `CONF-${blockA.id}-${blockB.id}`,
            sectionId: blockA.sectionId,
            blockA,
            blockB,
            severity: 'HIGH',
            message: `Conflict on ${blockA.sectionId}: ${blockA.department} (${blockA.id}) overlaps with ${blockB.department} (${blockB.id}) between ${Math.max(blockA.startHour, blockB.startHour)}:00 and ${Math.min(blockA.endHour, blockB.endHour)}:00.`,
          });
        }
      }
    }
  }

  return conflicts;
}