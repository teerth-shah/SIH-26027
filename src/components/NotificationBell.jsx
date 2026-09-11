import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { Bell, Send, CheckCircle2, X } from 'lucide-react';

export default function NotificationBell({ notifications, onOpen }) {
  const [open, setOpen] = useState(false);

  const unreadCount = notifications.filter((n) => !n.read).length;

  const handleOpen = () => {
    setOpen(true);
    onOpen();
  };

  return (
    <>
      <button
        onClick={handleOpen}
        className="relative text-slate-400 hover:text-blue-600 transition-colors"
      >
        <Bell size={18} />
        {unreadCount > 0 && (
          <span className="absolute -top-1.5 -right-1.5 bg-red-500 text-white text-[9px] font-bold rounded-full min-w-[16px] h-4 px-1 flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {open && createPortal(
        <div
          className="fixed inset-0 bg-slate-900/60 flex items-center justify-center z-[9999] px-4"
          onClick={() => setOpen(false)}
        >
          <div
            className="bg-white rounded-lg shadow-2xl w-full max-w-sm overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <h4 className="text-sm font-bold text-slate-800">Notifications</h4>
              <button
                onClick={() => setOpen(false)}
                className="text-slate-400 hover:text-slate-700 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            <div className="max-h-96 overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="px-5 py-10 text-center">
                  <Bell size={28} className="mx-auto text-slate-300 mb-2" />
                  <p className="text-xs text-slate-400 font-medium">No notifications yet</p>
                </div>
              ) : (
                notifications.map((n) => (
                  <div
                    key={n.id}
                    className={`px-5 py-3.5 border-b border-slate-50 last:border-b-0 flex items-start gap-3 ${
                      !n.read ? 'bg-blue-50/40' : ''
                    }`}
                  >
                    <div
                      className={`p-1.5 rounded-full shrink-0 mt-0.5 ${
                        n.type === 'approved' ? 'bg-teal-50 text-teal-600' : 'bg-blue-50 text-blue-600'
                      }`}
                    >
                      {n.type === 'approved' ? <CheckCircle2 size={14} /> : <Send size={14} />}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-semibold text-slate-700">{n.title}</p>
                      <p className="text-xs text-slate-500 mt-0.5">{n.message}</p>
                      <p className="text-[10px] text-slate-400 mt-1">{n.time}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>,
        document.body
      )}
    </>
  );
}