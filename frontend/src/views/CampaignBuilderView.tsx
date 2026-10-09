import React, { useState } from 'react';
import {
  Check,
  Smartphone,
  Monitor,
  Square,
  Zap
} from 'lucide-react';
import type { Product, BrandKit } from '../types';
import { SocialIcon } from '../components/SocialIcon';
import { api } from '../api/client';

interface CampaignBuilderViewProps {
  products: Product[];
  brandKit: BrandKit | null;
  onCampaignCreated: (campaignId: number) => void;
  onToast: (type: 'success' | 'error' | 'warning' | 'info', msg: string) => void;
}

export const CampaignBuilderView: React.FC<CampaignBuilderViewProps> = ({
  products,
  brandKit,
  onCampaignCreated,
  onToast
}) => {
  const [title, setTitle] = useState('');
  const [prompt, setPrompt] = useState('');
  const [selectedProductId, setSelectedProductId] = useState<number | null>(products[0]?.id || null);

  const [objective, setObjective] = useState('Conversions & Brand Awareness');
  const [cta, setCta] = useState('Shop Now');
  const [tone, setTone] = useState(brandKit?.tone_of_voice || 'Energetic & Modern');
  const [language, setLanguage] = useState('English');
  const [targetAudience, setTargetAudience] = useState(brandKit?.target_persona || 'Tech-forward Gen-Z and Millennials');

  const [videoFormat, setVideoFormat] = useState<string>('9:16');
  const [posterFormat, setPosterFormat] = useState<string>('1:1');

  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([
    'instagram',
    'facebook',
    'youtube'
  ]);

  const [isSubmitting, setIsSubmitting] = useState(false);

  // Quick Prompt Chips
  const promptPresets = [
    {
      label: '🔥 Summer Flash Sale 30% Off',
      prompt: 'Launch an energetic flash sale targeting active lifestyle customers. Emphasize limited discount and top-tier build quality.'
    },
    {
      label: '⚡ Next-Gen Tech Drop',
      prompt: 'Unveil an innovative flagship product drop focusing on high specs, effortless ergonomics, and beating high-priced market alternatives.'
    },
    {
      label: '🌿 Aesthetic Wellness & Clean Drop',
      prompt: 'Create a clean, soothing, aesthetic campaign focusing on everyday wellness, proven clinical results, and customer satisfaction.'
    },
    {
      label: '🎯 High-Performance Showcase',
      prompt: 'Highlight product design philosophy, premium materials, and high productivity utility for modern creators and professionals.'
    }
  ];

  const togglePlatform = (p: string) => {
    setSelectedPlatforms((prev) => {
      if (prev.includes(p)) {
        if (prev.length === 1) return prev; // Keep at least one
        return prev.filter((item) => item !== p);
      } else {
        return [...prev, p];
      }
    });
  };

  const handleLaunch = async () => {
    if (!title.trim()) {
      onToast('error', 'Please provide a campaign title');
      return;
    }
    if (!prompt.trim()) {
      onToast('error', 'Please provide a natural language campaign prompt');
      return;
    }
    if (!selectedProductId) {
      onToast('error', 'Please select at least one product from inventory');
      return;
    }
    if (selectedPlatforms.length === 0) {
      onToast('error', 'Please select at least one social media platform');
      return;
    }

    setIsSubmitting(true);
    try {
      // 1. Create Campaign
      const campaign = await api.createCampaign({
        title,
        prompt,
        product_ids: [selectedProductId],
        brand_kit_id: brandKit?.id,
        target_audience: targetAudience,
        tone,
        language,
        objective,
        cta,
        platforms: selectedPlatforms,
        video_format: videoFormat,
        poster_format: posterFormat
      });

      // 2. Trigger LangGraph Autonomous Workflow
      await api.triggerGenerate(campaign.id);

      onToast('success', `Campaign "${title}" created! LangGraph agent started.`);
      onCampaignCreated(campaign.id);
    } catch (err: any) {
      onToast('error', err.message || 'Failed to initialize campaign');
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">AI Campaign Builder</h1>
          <p className="page-subtitle">
            Configure social marketing campaign with parallel video & poster workflows powered by LangGraph
          </p>
        </div>

        <button
          id="launch-campaign-btn"
          className="btn btn-primary btn-lg"
          onClick={handleLaunch}
          disabled={isSubmitting}
        >
          <Zap size={18} /> {isSubmitting ? 'Initializing Agent...' : 'Launch AI Workflow'}
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
        {/* Step 1: Select Product */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 700 }}>1. Select Product from Inventory</h3>
            <span style={{ fontSize: '12px', color: '#94a3b8' }}>{products.length} products available</span>
          </div>

          <div className="grid-3">
            {products.map((p) => {
              const isSelected = selectedProductId === p.id;
              const imgUrl = p.image_urls?.[0] || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80';
              return (
                <div
                  key={p.id}
                  onClick={() => {
                    setSelectedProductId(p.id);
                    if (!title) setTitle(`${p.name} Launch Drop`);
                  }}
                  style={{
                    background: isSelected ? 'rgba(99, 102, 241, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                    border: `2px solid ${isSelected ? 'var(--accent-primary)' : 'var(--border-subtle)'}`,
                    borderRadius: 'var(--radius-md)',
                    padding: '14px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '14px',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <img
                    src={imgUrl}
                    alt={p.name}
                    style={{ width: '60px', height: '60px', objectFit: 'cover', borderRadius: '8px' }}
                  />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: '14px', fontWeight: 700, color: 'white', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {p.name}
                    </div>
                    <div style={{ fontSize: '12px', color: '#818cf8', marginTop: '2px' }}>
                      Rs. {p.price.toLocaleString('en-IN')} • {p.category}
                    </div>
                  </div>
                  {isSelected && (
                    <div style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      background: 'var(--accent-primary)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white'
                    }}>
                      <Check size={14} />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Step 2: Campaign Objective & Prompt */}
        <div className="glass-card">
          <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '16px' }}>
            2. Campaign Objective & Natural Language Prompt
          </h3>

          <div className="form-group">
            <label className="form-label">Campaign Title *</label>
            <input
              id="campaign-title-input"
              className="form-control"
              placeholder="e.g. AeroPulse Summer Soundwave Drop"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          {/* Prompt Presets */}
          <div style={{ marginBottom: '14px' }}>
            <span style={{ fontSize: '12px', color: '#94a3b8', display: 'block', marginBottom: '8px' }}>
              💡 Prompt Inspiration Templates:
            </span>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {promptPresets.map((preset, i) => (
                <button
                  key={i}
                  type="button"
                  className="btn btn-sm btn-secondary"
                  onClick={() => setPrompt(preset.prompt)}
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Describe Your Campaign *</label>
            <textarea
              id="campaign-prompt-input"
              className="form-control"
              rows={3}
              placeholder="Describe the campaign angle, key promotion, vibe, urgency, or specific hooks..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </div>

          <div className="grid-3">
            <div className="form-group">
              <label className="form-label">Primary Objective</label>
              <select
                className="form-control"
                value={objective}
                onChange={(e) => setObjective(e.target.value)}
              >
                <option value="Conversions & Brand Awareness">Conversions & Brand Awareness</option>
                <option value="Product Launch & Hype">Product Launch & Hype</option>
                <option value="Seasonal Flash Sale">Seasonal Flash Sale</option>
                <option value="Brand Storytelling">Brand Storytelling</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Call to Action (CTA)</label>
              <select
                className="form-control"
                value={cta}
                onChange={(e) => setCta(e.target.value)}
              >
                <option value="Shop Now">Shop Now</option>
                <option value="Claim 30% Off">Claim 30% Off</option>
                <option value="Learn More">Learn More</option>
                <option value="Get Early Access">Get Early Access</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Language</label>
              <input
                className="form-control"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              />
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Voice & Tone</label>
              <input
                className="form-control"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Target Audience Persona</label>
              <input
                className="form-control"
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Step 3: Media Format Selection (Single Video & Single Poster) */}
        <div className="glass-card">
          <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '6px' }}>
            3. Media Screen Size Selection
          </h3>
          <p style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '20px' }}>
            Select exactly one video screen size and one poster screen size. Poster and video will be generated in parallel workflows.
          </p>

          <div style={{ marginBottom: '22px' }}>
            <label className="form-label" style={{ marginBottom: '10px' }}>
              🎬 Video Screen Size (Select 1)
            </label>
            <div className="grid-3">
              {[
                { id: '9:16', title: '9:16 Vertical Video', sub: 'Reels, YouTube Shorts', icon: Smartphone, color: '#6366f1' },
                { id: '16:9', title: '16:9 Landscape Video', sub: 'YouTube Main Video', icon: Monitor, color: '#06b6d4' },
                { id: '1_1', title: '1:1 Square Video', sub: 'Feed Video (IG & FB)', icon: Square, color: '#ec4899' }
              ].map((fmt) => {
                const isSelected = videoFormat === fmt.id;
                const IconComponent = fmt.icon;
                return (
                  <div
                    key={fmt.id}
                    onClick={() => setVideoFormat(fmt.id)}
                    style={{
                      background: isSelected ? 'rgba(99, 102, 241, 0.18)' : 'rgba(255, 255, 255, 0.02)',
                      border: `2px solid ${isSelected ? 'var(--accent-primary)' : 'var(--border-subtle)'}`,
                      borderRadius: 'var(--radius-md)',
                      padding: '16px',
                      cursor: 'pointer',
                      textAlign: 'center',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <IconComponent size={26} color={fmt.color} style={{ margin: '0 auto 8px' }} />
                    <div style={{ fontWeight: 700, fontSize: '14px', color: 'white' }}>{fmt.title}</div>
                    <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>{fmt.sub}</div>
                    {isSelected && (
                      <div style={{ marginTop: '8px', fontSize: '11px', color: 'var(--accent-primary)', fontWeight: 700 }}>
                        ✓ Selected Video Format
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          <div>
            <label className="form-label" style={{ marginBottom: '10px' }}>
              🖼️ Promotional Poster Screen Size (Select 1)
            </label>
            <div className="grid-4">
              {[
                { id: '1:1', title: '1:1 Square Poster', sub: '1080 x 1080 (Feed)', color: '#ec4899' },
                { id: '4:5', title: '4:5 Portrait Post', sub: '1080 x 1350 (IG / FB)', color: '#a855f7' },
                { id: '16:9', title: '16:9 Banner Post', sub: '1200 x 675 (Wide)', color: '#06b6d4' },
                { id: '9:16', title: '9:16 Story Poster', sub: '1080 x 1920 (Story)', color: '#6366f1' }
              ].map((fmt) => {
                const isSelected = posterFormat === fmt.id;
                return (
                  <div
                    key={fmt.id}
                    onClick={() => setPosterFormat(fmt.id)}
                    style={{
                      background: isSelected ? 'rgba(99, 102, 241, 0.18)' : 'rgba(255, 255, 255, 0.02)',
                      border: `2px solid ${isSelected ? 'var(--accent-primary)' : 'var(--border-subtle)'}`,
                      borderRadius: 'var(--radius-md)',
                      padding: '16px',
                      cursor: 'pointer',
                      textAlign: 'center',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <Square size={24} color={fmt.color} style={{ margin: '0 auto 8px' }} />
                    <div style={{ fontWeight: 700, fontSize: '14px', color: 'white' }}>{fmt.title}</div>
                    <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>{fmt.sub}</div>
                    {isSelected && (
                      <div style={{ marginTop: '8px', fontSize: '11px', color: 'var(--accent-primary)', fontWeight: 700 }}>
                        ✓ Selected Poster Format
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Step 4: Destination Social Platforms */}
        <div className="glass-card">
          <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '6px' }}>
            4. Destination Social Platforms
          </h3>
          <p style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '16px' }}>
            Supported platforms: Instagram (video + poster), Facebook (video + poster), and YouTube (video only). Publishing executes in parallel.
          </p>

          <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap' }}>
            {[
              { id: 'instagram', label: 'Instagram', sub: 'Posts Video & Poster' },
              { id: 'facebook', label: 'Facebook', sub: 'Posts Video & Poster' },
              { id: 'youtube', label: 'YouTube', sub: 'Posts Video Only' }
            ].map((p) => {
              const isSelected = selectedPlatforms.includes(p.id);
              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => togglePlatform(p.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '14px 22px',
                    borderRadius: 'var(--radius-md)',
                    background: isSelected ? 'rgba(255, 255, 255, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                    border: `2px solid ${isSelected ? 'var(--accent-primary)' : 'var(--border-subtle)'}`,
                    color: isSelected ? 'white' : '#94a3b8',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: 600,
                    transition: 'all 0.2s ease'
                  }}
                >
                  <SocialIcon platform={p.id} size={20} />
                  <div style={{ textAlign: 'left' }}>
                    <div>{p.label}</div>
                    <div style={{ fontSize: '11px', color: '#94a3b8', fontWeight: 400 }}>{p.sub}</div>
                  </div>
                  {isSelected && <Check size={16} color="var(--accent-primary)" style={{ marginLeft: '6px' }} />}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
