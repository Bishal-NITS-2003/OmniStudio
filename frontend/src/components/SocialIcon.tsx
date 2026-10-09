import React from 'react';
import { Camera, Globe, Video, Smartphone, Share2 } from 'lucide-react';

interface SocialIconProps {
  platform: string;
  size?: number;
  color?: string;
}

export const SocialIcon: React.FC<SocialIconProps> = ({ platform, size = 18, color }) => {
  switch (platform.toLowerCase()) {
    case 'instagram':
      return <Camera size={size} color={color || '#ec4899'} />;
    case 'facebook':
      return (
        <svg
          width={size}
          height={size}
          viewBox="0 0 24 24"
          fill="none"
          stroke={color || "#1877f2"}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z" />
        </svg>
      );
    case 'youtube':
      return <Video size={size} color={color || '#ef4444'} />;
    case 'linkedin':
      return <Globe size={size} color={color || '#38bdf8'} />;
    case 'tiktok':
      return <Smartphone size={size} color={color || '#06b6d4'} />;
    default:
      return <Share2 size={size} color={color || '#6366f1'} />;
  }
};
