import React, { useState, useEffect } from 'react';
import {
  Download,
  Plus
} from 'lucide-react';
import type { PublishingAccount, Campaign } from '../types';
import { SocialIcon } from '../components/SocialIcon';
import { Modal } from '../components/Modal';
import { api } from '../api/client';

interface PublishingViewProps {
  campaigns: Campaign[];
  onToast: (type: 'success' | 'error' | 'warning' | 'info', msg: string) => void;
}

export const PublishingView: React.FC<PublishingViewProps> = ({
  campaigns,
  onToast
}) => {
  const [accounts, setAccounts] = useState<PublishingAccount[]>([]);

  // Connect Account Modal
  const [isConnectOpen, setIsConnectOpen] = useState(false);
  const [connectPlatform, setConnectPlatform] = useState('instagram');
  const [displayName, setDisplayName] = useState('');
  const [handle, setHandle] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [isMock, setIsMock] = useState(true);

  const fetchPublishingData = async () => {
    try {
      const accs = await api.getPublishingAccounts();
      setAccounts(accs);
    } catch {
      onToast('error', 'Failed to load publishing data');
    }
  };

  useEffect(() => {
    fetchPublishingData();
  }, []);

  const handleConnect = async () => {
    try {
      await api.connectAccount({
        platform: connectPlatform,
        display_name: displayName,
        handle,
        access_token: accessToken,
        is_mock: isMock
      });

      onToast('success', `Platform ${connectPlatform} account connected!`);
      setIsConnectOpen(false);
      fetchPublishingData();
    } catch {
      onToast('error', 'Failed to connect account');
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Social Media Hub & Publishing</h1>
          <p className="page-subtitle">
            Manage official API credentials, OAuth tokens, and audit published campaign drops
          </p>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => {
            setDisplayName('');
            setHandle('');
            setAccessToken('');
            setIsConnectOpen(true);
          }}
        >
          <Plus size={16} /> Connect Channel
        </button>
      </div>

      {/* Connected Channels Grid */}
      <div className="grid-3" style={{ marginBottom: '32px' }}>
        {accounts.map((acc) => (
          <div key={acc.id} className="glass-card" style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <div style={{
                background: 'rgba(255, 255, 255, 0.05)',
                padding: '10px',
                borderRadius: '10px'
              }}>
                <SocialIcon platform={acc.platform} size={22} />
              </div>
              <span className={`badge ${acc.is_connected ? 'badge-published' : 'badge-draft'}`}>
                {acc.is_connected ? (acc.is_mock ? 'SANDBOX ACTIVE' : 'LIVE API') : 'DISCONNECTED'}
              </span>
            </div>

            <h3 style={{ fontSize: '16px', fontWeight: 700, color: 'white' }}>{acc.display_name}</h3>
            <p style={{ fontSize: '13px', color: '#818cf8', marginBottom: '14px' }}>{acc.handle}</p>

            <div style={{
              background: 'rgba(0, 0, 0, 0.3)',
              borderRadius: '8px',
              padding: '10px 12px',
              fontSize: '11px',
              color: '#94a3b8',
              marginTop: 'auto'
            }}>
              <div><strong>Token:</strong> {acc.credentials_mask}</div>
              {acc.account_metadata?.followers && (
                <div style={{ marginTop: '2px' }}><strong>Audience:</strong> {acc.account_metadata.followers} followers</div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Export & Download Center */}
      <div className="glass-card" style={{ marginBottom: '32px' }}>
        <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '16px' }}>
          Asset Download & Package Center
        </h3>
        <p style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '20px' }}>
          When direct API posting permissions are not configured, download complete campaign packages
          including H.264 MP4 videos, promotional graphic posters, formatted caption text files, and storyboard plans.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {campaigns.map((c) => (
            <div
              key={c.id}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '14px 18px',
                background: 'rgba(255, 255, 255, 0.02)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-subtle)'
              }}
            >
              <div>
                <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'white' }}>{c.title}</h4>
                <p style={{ fontSize: '12px', color: '#94a3b8' }}>
                  {c.formats?.join(' • ')} • Status: {c.status}
                </p>
              </div>

              <a
                href={api.getDownloadUrl(c.id)}
                download
                className="btn btn-secondary btn-sm"
              >
                <Download size={14} /> Download Package (.ZIP)
              </a>
            </div>
          ))}
        </div>
      </div>

      {/* Connect Channel Modal */}
      <Modal
        isOpen={isConnectOpen}
        onClose={() => setIsConnectOpen(false)}
        title="Connect Social Media Channel"
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setIsConnectOpen(false)}>Cancel</button>
            <button className="btn btn-primary" onClick={handleConnect}>Save Channel</button>
          </>
        }
      >
        <div className="form-group">
          <label className="form-label">Platform</label>
          <select
            className="form-control"
            value={connectPlatform}
            onChange={(e) => setConnectPlatform(e.target.value)}
          >
            <option value="instagram">Instagram Graph API</option>
            <option value="facebook">Facebook Graph API</option>
            <option value="youtube">YouTube Data API v3</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Display Name</label>
          <input
            className="form-control"
            placeholder="e.g. Official Brand Instagram"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Handle / Username</label>
          <input
            className="form-control"
            placeholder="@yourbrand"
            value={handle}
            onChange={(e) => setHandle(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label className="form-label">OAuth Access Token (Optional for Live API)</label>
          <input
            type="password"
            className="form-control"
            placeholder="Bearer EAABwz..."
            value={accessToken}
            onChange={(e) => setAccessToken(e.target.value)}
          />
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '12px',
          background: 'rgba(99, 102, 241, 0.1)',
          borderRadius: '8px',
          border: '1px solid rgba(99, 102, 241, 0.2)'
        }}>
          <input
            type="checkbox"
            id="isMockCheckbox"
            checked={isMock}
            onChange={(e) => setIsMock(e.target.checked)}
            style={{ width: '16px', height: '16px' }}
          />
          <label htmlFor="isMockCheckbox" style={{ fontSize: '13px', color: '#c7d2fe', cursor: 'pointer' }}>
            Run in Demo / Sandbox Simulation Mode (No external API keys required)
          </label>
        </div>
      </Modal>
    </div>
  );
};
