import React, { useState } from 'react';
import { Send, FileText, MapPin, Clock, Wrench } from 'lucide-react';

export default function RequestForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    department: 'Engineering (P-Way)',
    taskType: 'Track Maintenance',
    section: 'Track 1 (Station A to B)',
    startTime: '',
    endTime: '',
    machine: 'None'
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

const handleSubmit = (e) => {
  e.preventDefault();

  const payload = {
    title: `${formData.taskType} - ${formData.department}`,
    section_id: formData.section.startsWith('Track 2') ? 2 : 1,
    duration_mins: 60
  };

  onSubmit(payload);

  alert(
    `Request Sent!\nDept: ${formData.department}\nTask: ${formData.taskType}`
  );
};

  onSubmit(payload);

  alert(
    `Request Sent!\nDept: ${formData.department}\nTask: ${formData.taskType}`
  );
};

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 h-full flex flex-col">
      <div className="flex items-center space-x-2 mb-4 border-b pb-3">
        <FileText className="text-blue-600" size={20} />
        <h3 className="font-bold text-slate-800">Submit Block Request</h3>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 flex-1 flex flex-col justify-between">
        <div>
          <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Department</label>
          <select name="department" onChange={handleChange} className="w-full p-2 border rounded bg-slate-50 text-sm mb-3">
            <option>Engineering (P-Way)</option>
            <option>Signaling (S&T)</option>
            <option>Electrical (OHE)</option>
          </select>

          <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Task Type</label>
          <select name="taskType" onChange={handleChange} className="w-full p-2 border rounded bg-slate-50 text-sm mb-3">
            <option>Track Maintenance</option>
            <option>OHE Maintenance</option>
            <option>Signal Calibration</option>
          </select>

          <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1 flex items-center gap-1"><MapPin size={12}/> Track Section</label>
          <select name="section" onChange={handleChange} className="w-full p-2 border rounded bg-slate-50 text-sm mb-3">
            <option>Track 1 (Station A to B)</option>
            <option>Track 2 (Station A to B)</option>
          </select>
        </div>

        <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-lg flex items-center justify-center space-x-2 transition-colors mt-2">
          <Send size={16} />
          <span>Send Request</span>
        </button>
      </form>
    </div>
  );
}
