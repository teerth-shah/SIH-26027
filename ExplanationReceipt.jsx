import React from 'react';
import { CheckCircle, Info, Trophy } from 'lucide-react';

export default function ExplanationReceipt({ explanationData }) {
  if (!explanationData) return null;

  return (
    <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden w-full">
      
      <div className="bg-slate-800 p-4 text-white flex items-center space-x-3">
        <Info size={20} className="text-blue-400" />
        <h3 className="font-semibold tracking-wide">AI SCHEDULING LOGIC</h3>
      </div>

      <div className="p-5">
        <p className="text-sm text-gray-500 mb-4 font-medium uppercase tracking-wider">
          Tasks Combined: {explanationData.combinedTasks.join(' + ')}
        </p>

        {/* Iterating through the array of reasons using map() */}
        <div className="space-y-3 mb-6">
          {explanationData.reasons.map((reason, index) => (
            <div key={index} className="flex items-start space-x-3">
              <CheckCircle size={18} className="text-green-500 flex-shrink-0 mt-0.5" />
              <span className="text-gray-700 text-sm">{reason}</span>
            </div>
          ))}
        </div>

        <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 flex items-center space-x-4">
          <div className="bg-blue-100 p-2 rounded-full text-blue-600">
            <Trophy size={24} />
          </div>
          <div>
            <p className="text-xs text-blue-600 font-bold uppercase tracking-wider">Impact</p>
            <p className="text-lg text-blue-900 font-extrabold">
              {explanationData.hoursSaved} Hours Saved!
            </p>
          </div>
        </div>

      </div>
    </div>
  );
} 