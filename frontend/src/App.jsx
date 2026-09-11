
import React, { useState, useEffect } from 'react';
import { LayoutDashboard, Calendar, Bell, Settings, User, Filter, Activity, ShieldCheck, Clock, Users } from 'lucide-react';

import RequestForm from './components/RequestForm';
import ConflictCard from './components/ConflictCard';
import ExplanationReceipt from './components/ExplanationReceipt';
import GanttTimeline from './components/GanttTimeline';
import CorridorMap from './components/CorridorMap';

import { MAINTENANCE_BLOCKS } from './mockData';

export default function App() {
// --- STATE ---
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedBlockId, setSelectedBlockId] = useState(null);
  const [isResolved, setIsResolved] = useState(false);
  const [filterTask, setFilterTask] = useState('ALL');
  const [activeUsers, setActiveUsers] = useState(142); // Starting number of users

  // --- HACKATHON DEMO TRICK: Simulate live user fluctuation ---
  useEffect(() => {
    const interval = setInterval(() => {
      // Randomly adds or subtracts 1 to 3 users every 5 seconds
      setActiveUsers(prev => prev + (Math.floor(Math.random() * 5) - 2)); 
    }, 5000);
    return () => clearInterval(interval);
  }, []);


  const displayBlocks = filterTask === 'ALL' 
    ? MAINTENANCE_BLOCKS 
    : MAINTENANCE_BLOCKS.filter(b => b.id === filterTask);

  const mockConflicts = isResolved ? [] : [
    { id: 'C-1', blockA: MAINTENANCE_BLOCKS[0], blockB: MAINTENANCE_BLOCKS[3] }
  ];
  
  const selectedBlockData = MAINTENANCE_BLOCKS.find(b => b.id === selectedBlockId);
  const isConflict = mockConflicts.some(c => c.blockA?.id === selectedBlockId || c.blockB?.id === selectedBlockId);

  return (
    <div className="flex h-screen bg-slate-50 font-sans overflow-hidden text-slate-800">
      
      {/* SIDEBAR */}
      <div className="w-64 bg-slate-900 text-slate-300 flex flex-col shadow-2xl z-20 border-r border-slate-800 shrink-0">
        <div className="p-6 border-b border-slate-800 bg-slate-900/50">
          <h1 className="text-2xl font-black tracking-wider text-white flex items-center gap-2">
            <Activity className="text-blue-500" size={24} />
            SIH-26027
          </h1>
          <p className="text-blue-400/80 text-[10px] font-bold uppercase tracking-widest mt-1.5">AI Block Planning Sys.</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-1.5 mt-2">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-md transition-all duration-200 ${
              activeTab === 'dashboard' ? 'bg-blue-700 text-white shadow-md' : 'hover:bg-slate-800 hover:text-white'
            }`}
          >
            <LayoutDashboard size={18} />
            <span className="font-semibold text-sm">Live Dashboard</span>
          </button>

          <button 
            onClick={() => setActiveTab('history')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-md transition-all duration-200 ${
              activeTab === 'history' ? 'bg-blue-700 text-white shadow-md' : 'hover:bg-slate-800 hover:text-white'
            }`}
          >
            <Calendar size={18} />
            <span className="font-semibold text-sm">Schedule History</span>
          </button>
        </nav>
        
        <div className="p-5 border-t border-slate-800 bg-slate-950/30 flex items-center space-x-3">
          <div className="bg-slate-800 p-2 rounded-md text-blue-400"><User size={16} /></div>
          <div>
            <p className="text-slate-500 text-[9px] uppercase font-bold tracking-wider">Session Active</p>
            <p className="font-bold text-slate-200 text-xs">Section Controller</p>
          </div>
        </div>
      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 flex flex-col overflow-auto z-10 relative">
        
{/* Top Header */}
        <header className="bg-white shadow-sm px-8 py-4 flex justify-between items-center sticky top-0 z-20 border-b border-slate-200 shrink-0">
          <div>
            <h2 className="text-lg font-bold text-slate-800">Divisional Overview</h2>
            <p className="text-xs text-slate-500 font-medium">Mumbai Railway Network</p>
          </div>
          <div className="flex space-x-5 items-center">
            
            {/* NEW: Live Active Users Badge */}
            <div className="flex items-center space-x-2 bg-slate-100 px-3 py-1.5 rounded-md border border-slate-200 shadow-sm transition-all duration-300">
              <Users size={14} className="text-blue-600" />
              <span className="text-[11px] font-bold text-slate-600 uppercase tracking-wide">
                <span className="text-blue-700 font-black">{activeUsers}</span> Active
              </span>
            </div>

            <button className="text-slate-400 hover:text-blue-600 transition-colors"><Bell size={18} /></button>
            <button className="text-slate-400 hover:text-blue-600 transition-colors"><Settings size={18} /></button>
            
            {/* AI Optimizer Badge */}
            <div className="flex items-center space-x-2 bg-teal-50 px-3 py-1.5 rounded-md border border-teal-200 shadow-sm">
              <span className="w-2 h-2 bg-teal-600 rounded-full animate-pulse"></span>
              <span className="text-[11px] font-bold text-teal-800 uppercase tracking-wide">Optimizer Online</span>
            </div>
            
          </div>
        </header>

        {activeTab === 'history' ? (
          <div className="flex-1 flex flex-col items-center justify-center animate-in fade-in duration-300">
            <Calendar size={48} className="text-slate-300 mb-4" />
            <h2 className="text-xl font-bold text-slate-700">Schedule History</h2>
            <p className="text-sm text-slate-500 mt-2">Database connection pending backend integration.</p>
          </div>
        ) : (
          <main className="p-6 flex-1 flex flex-col space-y-5 overflow-y-auto">
            
            {/* KPI RIBBON */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-1 shrink-0">
              <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 flex items-center space-x-4 border-l-4 border-l-blue-500">
                <div className="bg-slate-50 p-2.5 rounded text-blue-600"><LayoutDashboard size={20} /></div>
                <div><p className="text-[10px] font-bold text-slate-500 uppercase">Active Blocks</p><h4 className="text-lg font-black text-slate-800">{MAINTENANCE_BLOCKS.length}</h4></div>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 flex items-center space-x-4 border-l-4 border-l-red-500">
                <div className="bg-slate-50 p-2.5 rounded text-red-600"><ShieldCheck size={20} /></div>
                <div><p className="text-[10px] font-bold text-slate-500 uppercase">Conflicts Detected</p><h4 className="text-lg font-black text-slate-800">{mockConflicts.length}</h4></div>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 flex items-center space-x-4 border-l-4 border-l-teal-500">
                <div className="bg-slate-50 p-2.5 rounded text-teal-600"><Activity size={20} /></div>
                <div><p className="text-[10px] font-bold text-slate-500 uppercase">AI Efficiency</p><h4 className="text-lg font-black text-slate-800">98.5%</h4></div>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 flex items-center space-x-4 border-l-4 border-l-slate-700">
                <div className="bg-slate-50 p-2.5 rounded text-slate-700"><Clock size={20} /></div>
                <div><p className="text-[10px] font-bold text-slate-500 uppercase">Hours Saved</p><h4 className="text-lg font-black text-slate-800">12.5 hrs</h4></div>
              </div>
            </div>

            {/* FILTER TOOLBAR */}
            <div className="bg-white px-5 py-2.5 rounded-lg shadow-sm border border-slate-200 flex justify-between items-center z-10 shrink-0">
              <div className="flex items-center space-x-2 text-slate-700">
                <Filter size={16} />
                <span className="text-xs font-bold uppercase tracking-wide">Data Filter</span>
              </div>
              <select 
                value={filterTask} 
                onChange={(e) => setFilterTask(e.target.value)}
                className="bg-slate-50 border border-slate-200 text-slate-700 text-xs font-medium rounded-md focus:ring-blue-600 focus:border-blue-600 block p-2 cursor-pointer outline-none"
              >
                <option value="ALL">Show All Scheduled Tasks</option>
                {MAINTENANCE_BLOCKS.map(block => (
                  <option key={block.id} value={block.id}>{block.id}: {block.title} ({block.department})</option>
                ))}
              </select>
            </div>

            {/* ROW 1: THE MACRO VIEW (Fixed Exact Height) */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 h-[450px] shrink-0">
              <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden transition-all duration-300 h-full">
                <GanttTimeline selectedBlockId={selectedBlockId} onSelectBlock={setSelectedBlockId} filteredBlocks={displayBlocks} conflicts={mockConflicts} />
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-1 transition-all duration-300 h-full">
                <CorridorMap selectedBlockId={selectedBlockId} onSelectBlock={setSelectedBlockId} filteredBlocks={displayBlocks} />
              </div>
            </div>

            {/* ROW 2: THE MICRO VIEW (Minimum Height to prevent squeezing) */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 pb-8 min-h-[420px] shrink-0 items-stretch">
              <div className="lg:col-span-1 h-full">
                <RequestForm onSubmit={(data) => alert("Sending to Backend: " + JSON.stringify(data))} />
              </div>

              {/* Diagnostic Area */}
              <div className="lg:col-span-2 bg-slate-100/50 rounded-lg shadow-inner border border-slate-200 p-6 flex flex-col justify-center items-center relative overflow-hidden h-full">
                <h3 className="absolute top-4 left-5 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Diagnostic Engine</h3>
                
                <div className="w-full max-w-lg mt-4 transition-all duration-500 ease-in-out">
                  {!selectedBlockId && (
                    <div className="text-center py-10 opacity-60">
                      <LayoutDashboard size={40} className="mx-auto text-slate-400 mb-3" />
                      <p className="text-slate-500 text-sm font-medium">Select a block on the timeline or map to run diagnostics.</p>
                    </div>
                  )}

                  {selectedBlockId && isConflict && !isResolved && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                      <ConflictCard 
                        conflictData={{
                          severity: 'critical', type: 'Unsafe Track Overlap', description: `Critical resource and spatial conflict detected at ${selectedBlockData?.sectionId}.`, departments: ['Track', 'Civil'], overlapTime: `${selectedBlockData?.startHour}:00 - ${selectedBlockData?.endHour}:00`
                        }} 
                        onRunOptimizer={() => setIsResolved(true)} 
                      />
                    </div>
                  )}

                  {selectedBlockId && isResolved && (
                    <div className="animate-in fade-in zoom-in-95 duration-500">
                      <ExplanationReceipt 
                        explanationData={{
                          combinedTasks: ['Rail Grinding', 'Bridge Maintenance'], reasons: ['Same track section identified successfully.', 'Task types are operationally compatible.', 'Merged into safe Mega-Block.'], hoursSaved: 4
                        }} 
                      />
                    </div>
                  )}

                  {selectedBlockId && !isConflict && !isResolved && (
                    <div className="bg-white border-l-4 border-l-teal-500 shadow-sm p-5 rounded-r-md text-left mt-6 animate-in fade-in slide-in-from-bottom-4 duration-500 flex items-center space-x-4">
                      <div className="bg-teal-50 p-3 rounded-full"><ShieldCheck size={28} className="text-teal-600" /></div>
                      <div>
                        <h4 className="text-slate-800 font-black text-base">Safe Track Block Verified</h4>
                        <p className="text-slate-500 font-medium text-xs mt-0.5">Block {selectedBlockId} has no conflicts and is cleared for execution.</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>

          </main>
        )}
      </div>
    </div>
  );
}