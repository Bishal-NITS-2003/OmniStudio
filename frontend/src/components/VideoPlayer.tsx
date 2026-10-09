import React, { useState } from 'react';
import { Smartphone, Monitor, Square, Download, Volume2, Sparkles } from 'lucide-react';
import type { VideoAsset } from '../types';

interface VideoPlayerProps {
  videos?: VideoAsset[];
  fallbackPoster?: string;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({ videos = [], fallbackPoster }) => {
  const [selectedFormat, setSelectedFormat] = useState<'9:16' | '16:9' | '1:1'>('9:16');

  const activeVideo = videos.find(v => v.aspect_ratio.includes(selectedFormat.replace(':', '_')) || v.aspect_ratio === selectedFormat) || videos[0];

  const aspectClass =
    selectedFormat === '9:16' ? 'video-aspect-9-16' :
    selectedFormat === '16:9' ? 'video-aspect-16-9' : 'video-aspect-1-1';

  return (
    <div className="video-frame-wrapper">
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        marginBottom: '20px',
        background: 'rgba(255, 255, 255, 0.05)',
        padding: '6px',
        borderRadius: '12px'
      }}>
        <button
          className={`btn btn-sm ${selectedFormat === '9:16' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setSelectedFormat('9:16')}
        >
          <Smartphone size={14} /> 9:16 Reels/Shorts
        </button>
        <button
          className={`btn btn-sm ${selectedFormat === '16:9' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setSelectedFormat('16:9')}
        >
          <Monitor size={14} /> 16:9 Landscape
        </button>
        <button
          className={`btn btn-sm ${selectedFormat === '1:1' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setSelectedFormat('1:1')}
        >
          <Square size={14} /> 1:1 Square Feed
        </button>
      </div>

      <div className={`video-aspect-container ${aspectClass}`}>
        {activeVideo?.url ? (
          <video
            key={activeVideo.url}
            src={activeVideo.url}
            controls
            autoPlay
            loop
            muted
            playsInline
            className="video-player-element"
            poster={fallbackPoster}
          />
        ) : (
          <div style={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '24px',
            textAlign: 'center',
            background: 'linear-gradient(180deg, #090d16, #111827)'
          }}>
            <Sparkles size={40} color="#6366f1" style={{ marginBottom: '12px' }} />
            <h4 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '6px' }}>Ready to Render</h4>
            <p style={{ fontSize: '12px', color: '#94a3b8' }}>
              Launch generation to compose product transition video with audio backing.
            </p>
          </div>
        )}
      </div>

      {activeVideo && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          width: '100%',
          maxWidth: selectedFormat === '16:9' ? '640px' : '440px',
          marginTop: '16px',
          padding: '10px 16px',
          background: 'rgba(255, 255, 255, 0.04)',
          borderRadius: '10px',
          fontSize: '12px',
          color: '#cbd5e1'
        }}>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <span><strong>Res:</strong> {activeVideo.resolution}</span>
            <span><strong>Duration:</strong> {activeVideo.duration_seconds}s</span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#10b981' }}>
              <Volume2 size={13} /> BGM Audio Muxed
            </span>
          </div>

          <a
            href={activeVideo.url}
            download={activeVideo.filename}
            className="btn btn-secondary btn-sm"
            style={{ textDecoration: 'none' }}
          >
            <Download size={13} /> Download MP4
          </a>
        </div>
      )}
    </div>
  );
};
