import { fetchClient } from './client';

export const getDashboard = () => fetchClient('/api/dashboard');
export const getBlocks = () => fetchClient('/api/blocks');
export const getConflicts = () => fetchClient('/api/blocks'); // Fallback or use conflicts API if exists
export const getHistory = () => fetchClient('/api/history');
export const getLatestPlan = () => fetchClient('/api/planner/latest');
export const generatePlan = (data) => fetchClient('/api/planner/generate', {
  method: 'POST',
  body: JSON.stringify(data)
});
export const submitBlockRequest = (data) => fetchClient('/api/block-requests', {
  method: 'POST',
  body: JSON.stringify(data)
});
