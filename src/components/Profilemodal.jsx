import React from 'react';
import { createPortal } from 'react-dom';
import { X, Mail, Phone, IdCard, ShieldCheck, LogOut } from 'lucide-react';

export default function ProfileModal({ user, onClose, onLogout }) {
  if (!user) return null;

  return createPortal(
    <div
      className="fixed inset-0 bg-slate-900/60 flex items-center justify-center z-[9999] px-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg shadow-2xl w-full max-w-sm overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header band */}
        <div className="bg-slate-900 px-6 py-4 relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
          >
            <X size={18} />
          </button>
          <p className="text-blue-400 text-[10px] font-bold uppercase tracking-widest">Employee Profile</p>
        </div>

        {/* Avatar, fully below the band */}
        <div className="flex justify-center pt-6">
          <div className="w-20 h-20 rounded-full bg-slate-200 shadow-md flex items-center justify-center overflow-hidden">
            {user.photoUrl ? (
              <img src={user.photoUrl} alt={user.username} className="w-full h-full object-cover" />
            ) : (
              <span className="text-2xl font-bold text-slate-500">
                {user.username?.charAt(0).toUpperCase()}
              </span>
            )}
          </div>
        </div>

        {/* Body */}
        <div className="px-6 pt-3 pb-6">
          <div className="text-center mb-5">
            <h3 className="text-slate-800 font-bold text-base">{user.username}</h3>
            <p className="text-blue-700 text-xs font-semibold uppercase tracking-wide mt-0.5">{user.role}</p>
          </div>

          <div className="space-y-3">
            <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-md px-3 py-2.5">
              <IdCard size={16} className="text-slate-400 shrink-0" />
              <div className="min-w-0">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Employee ID</p>
                <p className="text-sm text-slate-700 font-medium truncate">{user.employeeId}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-md px-3 py-2.5">
              <Mail size={16} className="text-slate-400 shrink-0" />
              <div className="min-w-0">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Email</p>
                <p className="text-sm text-slate-700 font-medium truncate">{user.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-md px-3 py-2.5">
              <Phone size={16} className="text-slate-400 shrink-0" />
              <div className="min-w-0">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Phone</p>
                <p className="text-sm text-slate-700 font-medium truncate">{user.phone}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-md px-3 py-2.5">
              <ShieldCheck size={16} className="text-slate-400 shrink-0" />
              <div className="min-w-0">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Role</p>
                <p className="text-sm text-slate-700 font-medium truncate">{user.role}</p>
              </div>
            </div>
          </div>

          <button
            onClick={onLogout}
            className="w-full mt-6 flex items-center justify-center gap-2 bg-red-50 hover:bg-red-100 text-red-700 font-semibold text-sm py-2.5 rounded-md transition-colors"
          >
            <LogOut size={15} />
            Log out
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
}