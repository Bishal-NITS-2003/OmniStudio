import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Info, X } from 'lucide-react';

export interface ToastMessage {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  message: string;
}

interface ToastProps {
  toasts: ToastMessage[];
  onDismiss: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({ toasts, onDismiss }) => {
  if (toasts.length === 0) return null;

  return (
    <div style={{
      position: 'fixed',
      bottom: '24px',
      right: '24px',
      display: 'flex',
      flexDirection: 'column',
      gap: '10px',
      zIndex: 9999,
      maxWidth: '400px'
    }}>
      {toasts.map((t) => (
        <div
          key={t.id}
          style={{
            background: '#111827',
            border: `1px solid ${
              t.type === 'success' ? '#10b981' :
              t.type === 'error' ? '#f43f5e' :
              t.type === 'warning' ? '#f59e0b' : '#6366f1'
            }`,
            borderRadius: '12px',
            padding: '14px 18px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
            color: 'white',
            fontSize: '13px',
            fontWeight: 500,
            animation: 'fadeIn 0.2s ease'
          }}
        >
          {t.type === 'success' && <CheckCircle2 size={18} color="#10b981" />}
          {t.type === 'error' && <XCircle size={18} color="#f43f5e" />}
          {t.type === 'warning' && <AlertTriangle size={18} color="#f59e0b" />}
          {t.type === 'info' && <Info size={18} color="#6366f1" />}
          
          <span style={{ flex: 1 }}>{t.message}</span>
          
          <button
            onClick={() => onDismiss(t.id)}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#94a3b8',
              cursor: 'pointer',
              display: 'flex'
            }}
          >
            <X size={15} />
          </button>
        </div>
      ))}
    </div>
  );
};
