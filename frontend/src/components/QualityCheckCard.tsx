import React from 'react';
import { ShieldCheck, Check, AlertTriangle } from 'lucide-react';
import type { QualityReport } from '../types';

interface QualityCheckCardProps {
  report?: QualityReport;
}

export const QualityCheckCard: React.FC<QualityCheckCardProps> = ({ report }) => {
  if (!report) return null;

  const score = report.score || 95;
  const isPass = report.status === 'PASSED';

  return (
    <div className="glass-card" style={{ borderLeft: '4px solid #10b981' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            background: 'rgba(16, 185, 129, 0.15)',
            color: '#10b981',
            padding: '8px',
            borderRadius: '10px'
          }}>
            <ShieldCheck size={22} />
          </div>
          <div>
            <h4 style={{ fontSize: '16px', fontWeight: 700 }}>AI Quality & Compliance Gate</h4>
            <p style={{ fontSize: '12px', color: '#94a3b8' }}>Verified against specifications & social standards</p>
          </div>
        </div>

        <div style={{
          background: 'rgba(16, 185, 129, 0.12)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          borderRadius: '12px',
          padding: '8px 16px',
          textAlign: 'right'
        }}>
          <div style={{ fontSize: '20px', fontWeight: 800, color: '#10b981' }}>{score}/100</div>
          <div style={{ fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#6ee7b7', fontWeight: 700 }}>
            {isPass ? 'PASSED AUDIT' : 'REVIEW NEEDED'}
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {(report.checks || []).map((check, i) => (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px',
              padding: '10px 14px',
              background: 'rgba(255, 255, 255, 0.03)',
              borderRadius: '8px',
              border: '1px solid var(--border-subtle)'
            }}
          >
            <div style={{
              marginTop: '2px',
              color: check.status === 'PASS' ? '#10b981' : '#f59e0b'
            }}>
              {check.status === 'PASS' ? <Check size={16} /> : <AlertTriangle size={16} />}
            </div>
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: '#f1f5f9' }}>{check.name}</div>
              <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '2px' }}>{check.details}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
