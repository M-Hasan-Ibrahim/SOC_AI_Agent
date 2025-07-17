// src/utils.js
export const formatTimestamp = (timestamp) =>
  new Date(timestamp).toLocaleString();

export const formatIPAddress = (ip) => ip || 'Unknown';
