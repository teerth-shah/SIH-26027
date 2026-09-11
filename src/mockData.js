export const DEPARTMENT_COLORS = {
  Track: '#e53e3e',
  Electrical: '#dd6b20',
  Signaling: '#3182ce',
  Civil: '#38a169',
};

export const SECTIONS = [
  { id: 'SEC-01', name: 'Section A (Terminal - Central)', coords: [[19.0760, 72.8777], [19.1200, 72.8900]] },
  { id: 'SEC-02', name: 'Section B (Central - North)', coords: [[19.1200, 72.8900], [19.2000, 72.9700]] },
  { id: 'SEC-03', name: 'Section C (North - Junction)', coords: [[19.2000, 72.9700], [19.2800, 73.0500]] },
];

export const STATIONS = [
  { id: 'STN-01', name: 'Terminal A', position: [19.0760, 72.8777] },
  { id: 'STN-02', name: 'Central Hub', position: [19.1200, 72.8900] },
  { id: 'STN-03', name: 'North Station', position: [19.2000, 72.9700] },
  { id: 'STN-04', name: 'Junction B', position: [19.2800, 73.0500] },
];

export const MAINTENANCE_BLOCKS = [
  {
    id: 'BLK-101',
    sectionId: 'SEC-01',
    department: 'Track',
    title: 'Rail Grinding',
    day: 'Mon',
    startHour: 2,
    endHour: 6,
    locationCoords: [19.0980, 72.8840],
  },
  {
    id: 'BLK-102',
    sectionId: 'SEC-02',
    department: 'Electrical',
    title: 'OHE Inspection',
    day: 'Tue',
    startHour: 10,
    endHour: 15,
    locationCoords: [19.1690, 72.9415],
  },
  {
    id: 'BLK-103',
    sectionId: 'SEC-03',
    department: 'Signaling',
    title: 'Interlocking Test',
    day: 'Wed',
    startHour: 1,
    endHour: 5,
    locationCoords: [19.2590, 73.0215],
  },
  {
    id: 'BLK-104',
    sectionId: 'SEC-01',
    department: 'Civil',
    title: 'Bridge Maintenance',
    day: 'Mon',
    startHour: 4,
    endHour: 9,
    locationCoords: [19.0870, 72.8840],
  },
];