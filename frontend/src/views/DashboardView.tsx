import React from 'react';
import {
  Sparkles,
  Video,
  Send,
  ShieldCheck,
  Plus,
  ArrowRight,
  TrendingUp
} from 'lucide-react';
import type { AnalyticsOverview, Campaign } from '../types';
import { SocialIcon } from '../components/SocialIcon';

interface DashboardViewProps {
  analytics: AnalyticsOverview | null;
  campaigns: Campaign[];
  onSelectCampaign: (id: number) => void;
  onNavigate: (view: string) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  analytics,
  campaigns,
  onSelectCampaign,
  onNavigate
}) => {
  return (
    <div>
      {/* Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(236, 72, 153, 0.1))',
        border: '1px solid rgba(99, 102, 241, 0.3)',
        borderRadius: 'var(--radius-lg)',
        padding: '32px',
        marginBottom: '32px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ maxWidth: '640px', zIndex: 2 }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            background: 'rgba(99, 102, 241, 0.25)',
            color: '#a5b4fc',
            padding: '4px 12px',
            borderRadius: 'var(--radius-full)',
            fontSize: '12px',
            fontWeight: 700,
            marginBottom: '14px'
          }}>
            <Sparkles size={14} /> AUTONOMOUS MARKETING WORKFLOW
          </div>
          <h1 style={{ fontSize: '32px', fontWeight: 800, marginBottom: '10px' }}>
            Scale Omnichannel Drops with GenAI & LangGraph
          </h1>
          <p style={{ color: '#cbd5e1', fontSize: '15px', lineHeight: 1.6, marginBottom: '20px' }}>
            Transform product inventory into scene storyboards, multi-aspect ratio transition videos,
            persuasive copy, and scheduled cross-platform drops in minutes.
          </p>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              id="dash-create-btn"
              className="btn btn-primary btn-lg"
              onClick={() => onNavigate('builder')}
            >
              <Plus size={18} /> Launch New Campaign
            </button>
            <button
              id="dash-products-btn"
              className="btn btn-secondary btn-lg"
              onClick={() => onNavigate('products')}
            >
              Manage Products
            </button>
          </div>
        </div>

        <div style={{
          position: 'absolute',
          right: '-40px',
          top: '-40px',
          width: '260px',
          height: '260px',
          background: 'radial-gradient(circle, rgba(236, 72, 153, 0.25) 0%, transparent 70%)',
          borderRadius: '50%',
          pointerEvents: 'none'
        }} />
      </div>

      {/* KPI Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Campaigns Created</span>
            <div className="stat-icon"><Sparkles size={18} /></div>
          </div>
          <div className="stat-value">{analytics?.total_campaigns ?? campaigns.length}</div>
          <div className="stat-badge"><TrendingUp size={14} /> {analytics?.in_progress ?? 0} active now</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Videos Rendered</span>
            <div className="stat-icon"><Video size={18} /></div>
          </div>
          <div className="stat-value">{analytics?.total_videos_rendered ?? 2}</div>
          <div className="stat-badge"><TrendingUp size={14} /> 9:16 & 1:1 Formats</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Avg Quality Score</span>
            <div className="stat-icon" style={{ color: '#10b981', background: 'rgba(16, 185, 129, 0.12)' }}>
              <ShieldCheck size={18} />
            </div>
          </div>
          <div className="stat-value">{analytics?.average_qc_score ?? 96}%</div>
          <div className="stat-badge" style={{ color: '#10b981' }}>Claims & policy audited</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Published Drops</span>
            <div className="stat-icon" style={{ color: '#ec4899', background: 'rgba(236, 72, 153, 0.12)' }}>
              <Send size={18} />
            </div>
          </div>
          <div className="stat-value">{analytics?.published_campaigns ?? 1}</div>
          <div className="stat-badge">{analytics?.waiting_approval ?? 1} pending approval</div>
        </div>
      </div>

      {/* Recent Campaigns Section */}
      <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div>
            <h3 style={{ fontSize: '18px', fontWeight: 700 }}>Recent Marketing Campaigns</h3>
            <p style={{ fontSize: '13px', color: '#94a3b8' }}>Real-time execution status and asset preview</p>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={() => onNavigate('builder')}>
            <Plus size={14} /> New Campaign
          </button>
        </div>

        {campaigns.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>
            No campaigns found. Click "Launch New Campaign" to get started!
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {campaigns.map((c) => {
              const statusClass =
                c.status === 'PUBLISHED' ? 'badge-published' :
                c.status === 'WAITING_APPROVAL' ? 'badge-waiting' :
                c.status === 'APPROVED' ? 'badge-approved' :
                c.status === 'IN_PROGRESS' ? 'badge-progress' : 'badge-draft';

              return (
                <div
                  key={c.id}
                  onClick={() => onSelectCampaign(c.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '16px 20px',
                    background: 'rgba(255, 255, 255, 0.02)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.4)')}
                  onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--border-subtle)')}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{
                      width: '42px',
                      height: '42px',
                      borderRadius: '10px',
                      background: 'rgba(99, 102, 241, 0.15)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#a5b4fc'
                    }}>
                      <Sparkles size={20} />
                    </div>
                    <div>
                      <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'white' }}>{c.title}</h4>
                      <p style={{ fontSize: '12px', color: '#94a3b8', marginTop: '2px' }}>
                        Objective: {c.objective} • CTA: {c.cta}
                      </p>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      {(c.platforms || []).map((plat) => (
                        <SocialIcon key={plat} platform={plat} size={16} />
                      ))}
                    </div>

                    <span className={`badge ${statusClass}`}>
                      {c.status.replace('_', ' ')}
                    </span>

                    <ArrowRight size={16} color="#64748b" />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
