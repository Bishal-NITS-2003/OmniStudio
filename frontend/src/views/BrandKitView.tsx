import React, { useState, useEffect } from 'react';
import { Palette, Check, Sparkles, Plus, Trash2 } from 'lucide-react';
import type { BrandKit } from '../types';
import { api } from '../api/client';

interface BrandKitViewProps {
  brandKit: BrandKit | null;
  onRefresh: () => void;
  onToast: (type: 'success' | 'error' | 'warning' | 'info', msg: string) => void;
}

export const BrandKitView: React.FC<BrandKitViewProps> = ({
  brandKit,
  onRefresh,
  onToast
}) => {
  const [formData, setFormData] = useState<Partial<BrandKit>>({
    name: 'OmniNova Studio',
    primary_color: '#6366f1',
    secondary_color: '#ec4899',
    accent_color: '#06b6d4',
    background_color: '#0f172a',
    font_family: 'Inter',
    tone_of_voice: 'Energetic & Modern',
    target_persona: 'Tech-forward buyers and creative professionals looking for premium performance.',
    guidelines: [
      'High contrast text with rounded badge pill accents',
      'Hook viewers within the first 2 seconds of video',
      'Ensure call-to-action is prominent and clear'
    ]
  });

  const [newGuideline, setNewGuideline] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (brandKit) {
      setFormData(brandKit);
    }
  }, [brandKit]);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await api.updateBrandKit(formData);
      onToast('success', 'Brand Kit updated and synced with AI generation workflows!');
      onRefresh();
    } catch (err: any) {
      onToast('error', err.message || 'Failed to update brand kit');
    } finally {
      setIsSaving(false);
    }
  };

  const addGuideline = () => {
    if (!newGuideline.trim()) return;
    const current = formData.guidelines || [];
    setFormData({ ...formData, guidelines: [...current, newGuideline.trim()] });
    setNewGuideline('');
  };

  const removeGuideline = (index: number) => {
    const current = [...(formData.guidelines || [])];
    current.splice(index, 1);
    setFormData({ ...formData, guidelines: current });
  };

  const toneOptions = [
    'Energetic & Modern',
    'Luxury & Minimalist',
    'Bold & Disruptive',
    'Professional & Authoritative',
    'Playful & Humorous'
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Brand Kit & Creative System</h1>
          <p className="page-subtitle">
            Configure visual palette, voice guidelines, and design tokens applied to all media
          </p>
        </div>

        <button
          id="save-brand-kit-btn"
          className="btn btn-primary"
          onClick={handleSave}
          disabled={isSaving}
        >
          <Check size={16} /> {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      <div className="grid-2">
        {/* Visual Identity Section */}
        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <div style={{ background: 'rgba(99, 102, 241, 0.15)', padding: '8px', borderRadius: '10px', color: '#818cf8' }}>
              <Palette size={20} />
            </div>
            <div>
              <h3 style={{ fontSize: '17px', fontWeight: 700 }}>Brand Palette & Styling</h3>
              <p style={{ fontSize: '12px', color: '#94a3b8' }}>Colors utilized in video slides, badges & posters</p>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Brand Name</label>
            <input
              id="brand-name-input"
              className="form-control"
              value={formData.name || ''}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          {/* Color Pickers */}
          <div className="grid-2" style={{ gap: '16px', marginBottom: '20px' }}>
            <div>
              <label className="form-label">Primary Color</label>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <input
                  type="color"
                  value={formData.primary_color || '#6366f1'}
                  onChange={(e) => setFormData({ ...formData, primary_color: e.target.value })}
                  style={{ width: '40px', height: '40px', border: 'none', borderRadius: '8px', cursor: 'pointer', background: 'transparent' }}
                />
                <input
                  className="form-control"
                  value={formData.primary_color || ''}
                  onChange={(e) => setFormData({ ...formData, primary_color: e.target.value })}
                />
              </div>
            </div>

            <div>
              <label className="form-label">Secondary Color</label>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <input
                  type="color"
                  value={formData.secondary_color || '#ec4899'}
                  onChange={(e) => setFormData({ ...formData, secondary_color: e.target.value })}
                  style={{ width: '40px', height: '40px', border: 'none', borderRadius: '8px', cursor: 'pointer', background: 'transparent' }}
                />
                <input
                  className="form-control"
                  value={formData.secondary_color || ''}
                  onChange={(e) => setFormData({ ...formData, secondary_color: e.target.value })}
                />
              </div>
            </div>

            <div>
              <label className="form-label">Accent Highlight</label>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <input
                  type="color"
                  value={formData.accent_color || '#06b6d4'}
                  onChange={(e) => setFormData({ ...formData, accent_color: e.target.value })}
                  style={{ width: '40px', height: '40px', border: 'none', borderRadius: '8px', cursor: 'pointer', background: 'transparent' }}
                />
                <input
                  className="form-control"
                  value={formData.accent_color || ''}
                  onChange={(e) => setFormData({ ...formData, accent_color: e.target.value })}
                />
              </div>
            </div>

            <div>
              <label className="form-label">Dark Theme Background</label>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <input
                  type="color"
                  value={formData.background_color || '#0f172a'}
                  onChange={(e) => setFormData({ ...formData, background_color: e.target.value })}
                  style={{ width: '40px', height: '40px', border: 'none', borderRadius: '8px', cursor: 'pointer', background: 'transparent' }}
                />
                <input
                  className="form-control"
                  value={formData.background_color || ''}
                  onChange={(e) => setFormData({ ...formData, background_color: e.target.value })}
                />
              </div>
            </div>
          </div>

          {/* Color Preview Pill Bar */}
          <div style={{
            background: 'rgba(255, 255, 255, 0.03)',
            borderRadius: '12px',
            padding: '16px',
            border: '1px solid var(--border-subtle)'
          }}>
            <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8', fontWeight: 700 }}>
              Live Color Palette Harmony
            </span>
            <div style={{ display: 'flex', gap: '8px', marginTop: '10px', height: '36px', borderRadius: '8px', overflow: 'hidden' }}>
              <div style={{ flex: 2, background: formData.primary_color }} title="Primary" />
              <div style={{ flex: 1.5, background: formData.secondary_color }} title="Secondary" />
              <div style={{ flex: 1, background: formData.accent_color }} title="Accent" />
              <div style={{ flex: 2, background: formData.background_color }} title="Background" />
            </div>
          </div>
        </div>

        {/* Tone of Voice & Guidelines Section */}
        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <div style={{ background: 'rgba(236, 72, 153, 0.15)', padding: '8px', borderRadius: '10px', color: '#f472b6' }}>
              <Sparkles size={20} />
            </div>
            <div>
              <h3 style={{ fontSize: '17px', fontWeight: 700 }}>Voice & Creative Rules</h3>
              <p style={{ fontSize: '12px', color: '#94a3b8' }}>Guides LLM tone and narrative scripting</p>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Tone of Voice</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '12px' }}>
              {toneOptions.map((tone) => (
                <button
                  key={tone}
                  type="button"
                  className={`btn btn-sm ${formData.tone_of_voice === tone ? 'btn-primary' : 'btn-secondary'}`}
                  onClick={() => setFormData({ ...formData, tone_of_voice: tone })}
                >
                  {tone}
                </button>
              ))}
            </div>
            <input
              className="form-control"
              value={formData.tone_of_voice || ''}
              onChange={(e) => setFormData({ ...formData, tone_of_voice: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Target Audience Persona</label>
            <textarea
              className="form-control"
              rows={3}
              value={formData.target_persona || ''}
              onChange={(e) => setFormData({ ...formData, target_persona: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Reusable Creative Guidelines</label>
            <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
              <input
                className="form-control"
                placeholder="Add rule (e.g. Always include 30-day money back guarantee)..."
                value={newGuideline}
                onChange={(e) => setNewGuideline(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addGuideline(); }}}
              />
              <button className="btn btn-secondary" onClick={addGuideline}>
                <Plus size={16} />
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {(formData.guidelines || []).map((guide, i) => (
                <div
                  key={i}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '8px 12px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    borderRadius: '8px',
                    fontSize: '13px',
                    border: '1px solid var(--border-subtle)'
                  }}
                >
                  <span>• {guide}</span>
                  <button
                    onClick={() => removeGuideline(i)}
                    style={{ background: 'transparent', border: 'none', color: '#f43f5e', cursor: 'pointer' }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
