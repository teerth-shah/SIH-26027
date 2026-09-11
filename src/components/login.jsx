import React, { useState } from 'react';
import { Activity, Lock, Mail, AlertCircle } from 'lucide-react';

export default function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('operator@railways.gov.in');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    if (username.trim() === 'operator@railways.gov.in' && password === 'admin123') {
      setError('');
      onLoginSuccess({
        username: username.trim(),
        role: 'Section Controller',
        email: username.trim(),
        phone: '+91 98765 43210',
        employeeId: 'CR-EMP-4471',
        photoUrl: null,
      });
    } else {
      setError('Invalid credentials. Use operator@railways.gov.in / admin123');
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-slate-900 font-sans px-4">
      <div className="w-full max-w-sm">

        {/* Brand mark */}
        <div className="flex items-center gap-2.5 mb-8 justify-center">
          <div className="bg-blue-700 p-2 rounded-md">
            <Activity className="text-white" size={20} />
          </div>
          <div>
            <h1 className="text-white font-black text-lg leading-tight tracking-wide">SIH-26027</h1>
            <p className="text-blue-400 text-[10px] font-bold uppercase tracking-widest leading-tight">AI Block Planning Sys.</p>
          </div>
        </div>

        {/* Card */}
        <div className="bg-white rounded-lg shadow-2xl border border-slate-800 p-7">
          <h2 className="text-slate-800 font-bold text-base mb-1">Sign in to continue</h2>
          <p className="text-slate-500 text-xs font-medium mb-6">Divisional operations portal — Mumbai Railway Network</p>

          {error && (
            <div className="flex items-start gap-2 bg-red-50 border border-red-200 text-red-700 text-xs font-medium px-3 py-2.5 rounded-md mb-5">
              <AlertCircle size={14} className="shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-600 mb-1.5">Official Email / User ID</label>
              <div className="relative">
                <Mail size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  className="w-full pl-9 pr-3 py-2.5 rounded-md border border-slate-300 text-sm text-slate-800 outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-600 mb-1.5">Password</label>
              <div className="relative">
                <Lock size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full pl-9 pr-3 py-2.5 rounded-md border border-slate-300 text-sm text-slate-800 outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-700 hover:bg-blue-800 text-white font-semibold text-sm py-2.5 rounded-md transition-colors"
            >
              Sign in
            </button>
          </form>

          <div className="mt-5 pt-4 border-t border-slate-200 text-center">
            <p className="text-[11px] text-slate-400">
              Demo access: <span className="font-mono text-slate-500">operator@railways.gov.in</span> / <span className="font-mono text-slate-500">admin123</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}