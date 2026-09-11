import React from 'react';
import { AlertTriangle, Wrench, Clock, Zap } from 'lucide-react';

export default function ConflictCard({ conflictData, onRunOptimizer, isOptimizing }) {
  // If no data is passed in, render nothing
  if (!conflictData) return null;

  // Dynamically set CSS classes based on the severity string
  const isCritical = conflictData.severity === 'critical';
  const bgColor = isCritical ? 'bg-red-50 border-red-200' : 'bg-orange-50 border-orange-200';
  const textColor = isCritical ? 'text-red-700' : 'text-orange-700';
  const iconColor = isCritical ? 'text-red-500' : 'text-orange-500';

  return (
    <div className={`p-5 rounded-xl border-l-4 shadow-sm w-full ${bgColor} ${isCritical ? 'border-l-red-500' : 'border-l-orange-500'}`}>
      
      <div className="flex items-center space-x-3 mb-3">
        <AlertTriangle className={`${iconColor}`} size={24} />
        <h3 className={`font-bold text-lg ${textColor}`}>
          {isCritical ? 'CRITICAL CONFLICT' : 'WARNING DETECTED'}
        </h3>
      </div>

      <p className="text-gray-700 text-sm mb-4">
        <span className="font-semibold">{conflictData.type}: </span> 
        {conflictData.description}
      </p>

      <div className="bg-white p-3 rounded-md mb-4 border border-gray-100 space-y-2 text-sm text-gray-600">
        <div className="flex items-center space-x-2">
           <Wrench size={16} className="text-gray-400"/>
           <span>Depts: {conflictData.departments.join(' vs ')}</span>
        </div>
        <div className="flex items-center space-x-2">
           <Clock size={16} className="text-gray-400"/>
           <span>Overlap: {conflictData.overlapTime}</span>
        </div>
      </div>

      <button 
        onClick={onRunOptimizer}
        disabled={isOptimizing}
        className={`w-full flex items-center justify-center space-x-2 py-2 px-4 rounded-lg text-white font-medium transition-colors shadow-sm
          ${isCritical ? 'bg-red-600 hover:bg-red-700' : 'bg-orange-600 hover:bg-orange-700'}
          ${isOptimizing ? 'opacity-70 cursor-not-allowed' : ''}`}
      >
        <Zap size={18} className={isOptimizing ? "animate-pulse" : ""} />
        <span>{isOptimizing ? 'Optimizing...' : 'Run AI Optimizer'}</span>
      </button>
      
    </div>
  );
}