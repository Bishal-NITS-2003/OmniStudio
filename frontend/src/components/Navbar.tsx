import React from 'react';
import {
  LayoutDashboard,
  ShoppingBag,
  Sparkles,
  Palette,
  Share2,
  Cpu
} from 'lucide-react';

interface NavbarProps {
  currentView: string;
  onNavigate: (view: string) => void;
  campaignsCount?: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentView,
  onNavigate
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'products', label: 'Product Inventory', icon: ShoppingBag },
    { id: 'builder', label: 'AI Campaign Builder', icon: Sparkles },
    { id: 'brandkit', label: 'Brand Kit', icon: Palette },
    { id: 'publishing', label: 'Publishing & Channels', icon: Share2 },
  ];

  return (
    <aside className="sidebar">
      {/* Brand Header */}
      <div className="brand-logo" onClick={() => onNavigate('dashboard')} style={{ cursor: 'pointer' }}>
        <div className="brand-icon">
          <Cpu size={22} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span className="brand-title">OmniPost</span>
            <span className="brand-tag">AI</span>
          </div>
          <span style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginTop: '1px' }}>
            LangGraph Studio
          </span>
        </div>
      </div>

      {/* Nav items */}
      <div className="nav-group">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              className={`nav-link ${isActive ? 'active' : ''}`}
              onClick={() => onNavigate(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      {/* System Status Pill */}
      <div style={{
        marginTop: 'auto',
        background: 'rgba(255, 255, 255, 0.03)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: '14px',
        fontSize: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 8px #10b981' }} />
          <span style={{ fontWeight: 600, color: '#f1f5f9' }}>Demo Sandbox Mode</span>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '11px', lineHeight: 1.4 }}>
          Zero paid API keys needed. FFmpeg transitions + smart local agents active.
        </p>
      </div>
    </aside>
  );
};
