import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Download,
  CheckCircle,
  Copy,
  Layers,
  FileText,
  Clock,
  RefreshCw,
  ExternalLink,
  ChevronLeft,
  Share2
} from 'lucide-react';
import type { Campaign } from '../types';
import { StepperProgress } from '../components/StepperProgress';
import { VideoPlayer } from '../components/VideoPlayer';
import { QualityCheckCard } from '../components/QualityCheckCard';
import { Modal } from '../components/Modal';
import { api } from '../api/client';

interface CampaignDetailViewProps {
  campaignId: number;
  onBack: () => void;
  onToast: (type: 'success' | 'error' | 'warning' | 'info', msg: string) => void;
}

export const CampaignDetailView: React.FC<CampaignDetailViewProps> = ({
  campaignId,
  onBack,
  onToast
}) => {
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeMediaTab, setActiveMediaTab] = useState<'video' | 'poster' | 'carousel' | 'captions' | 'storyboard'>('video');
  const [activeCaptionPlatform, setActiveCaptionPlatform] = useState<string>('instagram');

  // Approval Modal
  const [isRevisionModalOpen, setIsRevisionModalOpen] = useState(false);
  const [revisionFeedback, setRevisionFeedback] = useState('');
  const [isPublishing, setIsPublishing] = useState(false);

  const fetchCampaign = async () => {
    try {
      const data = await api.getCampaign(campaignId);
      setCampaign(data);
    } catch {
      onToast('error', 'Failed to load campaign');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCampaign();
    const interval = setInterval(() => {
      if (campaign?.status === 'IN_PROGRESS') {
        fetchCampaign();
      }
    }, 2500);
    return () => clearInterval(interval);
  }, [campaignId, campaign?.status]);

  const handleApprove = async () => {
    try {
      await api.approveCampaign(campaignId, true);
      onToast('success', 'Campaign approved! Dispatching to destination channels.');
      setIsPublishing(true);
      await api.publishCampaign(campaignId);
      onToast('success', 'Published to social platforms!');
      fetchCampaign();
    } catch (err: any) {
      onToast('error', err.message || 'Approval failed');
    } finally {
      setIsPublishing(false);
    }
  };

  const handleRequestRevision = async () => {
    try {
      await api.approveCampaign(campaignId, false, revisionFeedback);
      onToast('info', 'Revision requested. Status updated.');
      setIsRevisionModalOpen(false);
      fetchCampaign();
    } catch {
      onToast('error', 'Failed to request revision');
    }
  };

  const handleRerun = async () => {
    try {
      await api.triggerGenerate(campaignId);
      onToast('info', 'Re-executing LangGraph generation pipeline...');
      fetchCampaign();
    } catch {
      onToast('error', 'Failed to re-run workflow');
    }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    onToast('success', `${label} copied to clipboard!`);
  };

  if (isLoading || !campaign) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 20px', color: '#94a3b8' }}>
        <RefreshCw className="animate-spin" size={32} style={{ margin: '0 auto 16px' }} />
        <p>Loading campaign details & pipeline artifacts...</p>
      </div>
    );
  }

  const assets = campaign.generated_assets || {};
  const captions = assets.captions || {};
  const videoAsset = assets.video || (assets.videos && assets.videos[0]);
  const posterAsset = assets.poster || (assets.posters && assets.posters[0]);
  const videos = videoAsset ? [videoAsset] : (assets.videos || []);
  const posters = posterAsset ? [posterAsset] : (assets.posters || []);
  const carouselSlides = assets.carousel_slides || [];

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <button
          className="btn btn-secondary btn-sm"
          onClick={onBack}
          style={{ marginBottom: '14px' }}
        >
          <ChevronLeft size={16} /> Back to Dashboard
        </button>

        <div className="page-header" style={{ marginBottom: '12px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
              <h1 className="page-title">{campaign.title}</h1>
              <span className={`badge badge-${campaign.status.toLowerCase().replace('_', '-')}`}>
                {campaign.status.replace('_', ' ')}
              </span>
            </div>
            <p className="page-subtitle">
              Prompt: "{campaign.prompt}"
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <a
              href={api.getDownloadUrl(campaign.id)}
              download
              className="btn btn-secondary"
              style={{ textDecoration: 'none' }}
            >
              <Download size={16} /> Download Package (.ZIP)
            </a>

            {campaign.status === 'WAITING_APPROVAL' && (
              <>
                <button
                  className="btn btn-danger"
                  onClick={() => setIsRevisionModalOpen(true)}
                >
                  Request Edits
                </button>
                <button
                  id="approve-publish-btn"
                  className="btn btn-success"
                  onClick={handleApprove}
                  disabled={isPublishing}
                >
                  <CheckCircle size={16} /> {isPublishing ? 'Publishing...' : 'Approve & Publish'}
                </button>
              </>
            )}

            {(campaign.status === 'DRAFT' || campaign.status === 'FAILED') && (
              <button className="btn btn-primary" onClick={handleRerun}>
                <RefreshCw size={16} /> Run Pipeline
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="glass-card" style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sparkles size={16} color="#6366f1" />
            <h3 style={{ fontSize: '15px', fontWeight: 700 }}>LangGraph Execution Pipeline</h3>
          </div>
          <span style={{ fontSize: '12px', color: '#94a3b8' }}>
            Active Node: <strong>{campaign.current_step}</strong>
          </span>
        </div>

        <StepperProgress currentStep={campaign.current_step} status={campaign.status} />

        <div style={{
          background: 'rgba(0, 0, 0, 0.4)',
          borderRadius: '10px',
          padding: '12px 16px',
          maxHeight: '130px',
          overflowY: 'auto',
          fontSize: '12px',
          fontFamily: 'monospace',
          border: '1px solid rgba(255, 255, 255, 0.05)'
        }}>
          {(campaign.step_logs || []).map((log, i) => (
            <div key={i} style={{ color: '#94a3b8', marginBottom: '4px' }}>
              <span style={{ color: '#6366f1' }}>[{log.step}]</span> {log.message}
            </div>
          ))}
        </div>
      </div>

      <div className="grid-2" style={{ alignItems: 'start', marginBottom: '32px' }}>
        <div className="glass-card">
          <div style={{
            display: 'flex',
            gap: '8px',
            borderBottom: '1px solid var(--border-subtle)',
            paddingBottom: '14px',
            marginBottom: '20px',
            overflowX: 'auto'
          }}>
            <button
              className={`btn btn-sm ${activeMediaTab === 'video' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveMediaTab('video')}
            >
              Product Video ({videos.length})
            </button>
            <button
              className={`btn btn-sm ${activeMediaTab === 'poster' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveMediaTab('poster')}
            >
              Promo Poster
            </button>
            <button
              className={`btn btn-sm ${activeMediaTab === 'carousel' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveMediaTab('carousel')}
            >
              <Layers size={13} /> Carousel ({carouselSlides.length})
            </button>
            <button
              className={`btn btn-sm ${activeMediaTab === 'captions' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveMediaTab('captions')}
            >
              <FileText size={13} /> Social Copy
            </button>
            <button
              className={`btn btn-sm ${activeMediaTab === 'storyboard' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveMediaTab('storyboard')}
            >
              Storyboard
            </button>
          </div>

          {activeMediaTab === 'video' && (
            <VideoPlayer
              videos={videos}
              fallbackPoster={posters[0]?.url}
            />
          )}

          {activeMediaTab === 'poster' && (
            <div style={{ textAlign: 'center' }}>
              {posters[0]?.url ? (
                <div>
                  <img
                    src={posters[0].url}
                    alt="Promo Poster"
                    style={{
                      width: '100%',
                      maxWidth: '440px',
                      borderRadius: 'var(--radius-md)',
                      boxShadow: '0 20px 40px rgba(0,0,0,0.5)',
                      border: '1px solid rgba(255,255,255,0.1)'
                    }}
                  />
                  <div style={{ marginTop: '16px' }}>
                    <a
                      href={posters[0].url}
                      download={posters[0].filename}
                      className="btn btn-secondary btn-sm"
                    >
                      <Download size={14} /> Download Poster Image
                    </a>
                  </div>
                </div>
              ) : (
                <p style={{ color: '#94a3b8', padding: '40px' }}>Generating promotional poster...</p>
              )}
            </div>
          )}

          {activeMediaTab === 'carousel' && (
            <div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '14px' }}>
                {carouselSlides.map((slide, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: 'rgba(255, 255, 255, 0.03)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: 'var(--radius-md)',
                      padding: '18px',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      minHeight: '140px'
                    }}
                  >
                    <div>
                      <span style={{ fontSize: '10px', background: 'rgba(99, 102, 241, 0.2)', color: '#a5b4fc', padding: '3px 8px', borderRadius: '4px', fontWeight: 700 }}>
                        {slide.tag || `SLIDE 0${slide.slide}`}
                      </span>
                      <h4 style={{ fontSize: '15px', fontWeight: 700, marginTop: '10px', color: 'white' }}>
                        {slide.title}
                      </h4>
                      <p style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '6px' }}>
                        {slide.bullet}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeMediaTab === 'captions' && (
            <div>
              <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
                {Object.keys(captions).map((plat) => (
                  <button
                    key={plat}
                    className={`btn btn-sm ${activeCaptionPlatform === plat ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveCaptionPlatform(plat)}
                  >
                    {plat.toUpperCase()}
                  </button>
                ))}
              </div>

              {captions[activeCaptionPlatform] && (
                <div style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '20px'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                    <span style={{ fontSize: '12px', color: '#818cf8', fontWeight: 600 }}>
                      Hook: {captions[activeCaptionPlatform].hook}
                    </span>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => copyToClipboard(captions[activeCaptionPlatform].caption, 'Caption')}
                    >
                      <Copy size={13} /> Copy Caption
                    </button>
                  </div>

                  <p style={{
                    fontSize: '14px',
                    color: '#e2e8f0',
                    lineHeight: 1.6,
                    whiteSpace: 'pre-wrap',
                    background: 'rgba(0,0,0,0.3)',
                    padding: '14px',
                    borderRadius: '8px'
                  }}>
                    {captions[activeCaptionPlatform].caption}
                  </p>

                  <div style={{ marginTop: '14px' }}>
                    <span style={{ fontSize: '12px', color: '#94a3b8', display: 'block', marginBottom: '6px' }}>
                      Optimized Hashtags:
                    </span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {(captions[activeCaptionPlatform].hashtags || []).map((ht: string, i: number) => (
                        <span key={i} style={{ fontSize: '11px', background: 'rgba(99, 102, 241, 0.15)', color: '#c7d2fe', padding: '3px 8px', borderRadius: '4px' }}>
                          {ht}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeMediaTab === 'storyboard' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {(campaign.storyboard || []).map((sc, i) => (
                <div
                  key={i}
                  style={{
                    padding: '14px 18px',
                    background: 'rgba(255, 255, 255, 0.02)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '10px'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: '#06b6d4' }}>
                      {sc.badge} • SCENE {sc.scene_number}
                    </span>
                    <span style={{ fontSize: '11px', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Clock size={12} /> {sc.duration}s
                    </span>
                  </div>
                  <h4 style={{ fontSize: '15px', fontWeight: 700, color: 'white' }}>{sc.title}</h4>
                  <p style={{ fontSize: '13px', color: '#cbd5e1', marginTop: '2px' }}>{sc.subtitle}</p>
                  {sc.visual_prompt && (
                    <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '6px', fontStyle: 'italic' }}>
                      Visual Cue: {sc.visual_prompt}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <QualityCheckCard report={campaign.quality_report} />

          {campaign.product_analysis && (
            <div className="glass-card">
              <h4 style={{ fontSize: '15px', fontWeight: 700, marginBottom: '12px' }}>
                AI Strategic Positioning & Hooks
              </h4>
              <p style={{ fontSize: '13px', color: '#cbd5e1', lineHeight: 1.5, marginBottom: '12px' }}>
                {campaign.product_analysis.core_value_prop}
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {(campaign.product_analysis.key_usps || []).map((usp: string, i: number) => (
                  <div key={i} style={{ fontSize: '12px', color: '#94a3b8', display: 'flex', gap: '6px' }}>
                    <span style={{ color: '#10b981' }}>✓</span> {usp}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="glass-card">
            <h4 style={{ fontSize: '15px', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Share2 size={16} color="#6366f1" /> Social Media Publishing Confirmations
            </h4>

            {(!campaign.published_records || campaign.published_records.length === 0) ? (
              <div style={{ fontSize: '13px', color: '#94a3b8' }}>
                Campaign pending approval. Click "Approve & Publish" above to dispatch to connected platforms.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {campaign.published_records.map((rec, i) => (
                  <div
                    key={i}
                    style={{
                      padding: '12px 14px',
                      background: 'rgba(255, 255, 255, 0.03)',
                      borderRadius: '8px',
                      border: '1px solid var(--border-subtle)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: rec.posts && rec.posts.length > 0 ? '8px' : '0' }}>
                      <div>
                        <div style={{ fontSize: '13px', fontWeight: 600, color: 'white' }}>
                          {rec.platform.toUpperCase()}
                        </div>
                        <div style={{ fontSize: '11px', color: '#94a3b8' }}>
                          Status: <span style={{ color: '#10b981' }}>{rec.status}</span> {rec.is_mock && '• Demo Sandbox'}
                        </div>
                      </div>
                      {rec.post_url && (!rec.posts || rec.posts.length === 0) && (
                        <a
                          href={rec.post_url}
                          target="_blank"
                          rel="noreferrer"
                          className="btn btn-secondary btn-sm"
                        >
                          <ExternalLink size={12} /> View Post
                        </a>
                      )}
                    </div>

                    {rec.posts && rec.posts.length > 0 && (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '6px' }}>
                        {rec.posts.map((p, pIdx) => (
                          <div
                            key={pIdx}
                            style={{
                              display: 'flex',
                              justifyContent: 'space-between',
                              alignItems: 'center',
                              background: 'rgba(0,0,0,0.25)',
                              padding: '6px 10px',
                              borderRadius: '6px',
                              fontSize: '12px'
                            }}
                          >
                            <span style={{ color: '#cbd5e1' }}>
                              {p.type.replace('_', ' ')}: <code style={{ color: '#818cf8' }}>{p.post_id}</code>
                            </span>
                            <a
                              href={p.url}
                              target="_blank"
                              rel="noreferrer"
                              className="btn btn-secondary btn-sm"
                              style={{ padding: '4px 8px', fontSize: '11px' }}
                            >
                              <ExternalLink size={11} /> Open
                            </a>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <Modal
        isOpen={isRevisionModalOpen}
        onClose={() => setIsRevisionModalOpen(false)}
        title="Request Campaign Revisions"
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setIsRevisionModalOpen(false)}>Cancel</button>
            <button className="btn btn-danger" onClick={handleRequestRevision}>Submit Edits</button>
          </>
        }
      >
        <div className="form-group">
          <label className="form-label">Feedback & Adjustment Instructions</label>
          <textarea
            className="form-control"
            rows={4}
            placeholder="Explain what needs to change (e.g. Make tone more humorous, change the primary hook, shorten video duration)..."
            value={revisionFeedback}
            onChange={(e) => setRevisionFeedback(e.target.value)}
          />
        </div>
      </Modal>
    </div>
  );
};
