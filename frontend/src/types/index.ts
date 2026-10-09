export interface Product {
  id: number;
  name: string;
  tagline?: string;
  description: string;
  category: string;
  price: number;
  currency: string;
  brand_name: string;
  features: string[];
  image_urls: string[];
  tags: string[];
  source_url?: string;
  created_at: string;
  updated_at: string;
}

export interface ProductImportResponse {
  name: string;
  tagline?: string;
  description: string;
  category: string;
  price: number;
  currency: string;
  brand_name: string;
  features: string[];
  image_urls: string[];
  source_url: string;
  extracted_source: string;
  confidence_score: number;
}

export interface BrandKit {
  id: number;
  name: string;
  logo_url?: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  background_color: string;
  font_family: string;
  tone_of_voice: string;
  target_persona: string;
  guidelines: string[];
  created_at: string;
  updated_at: string;
}

export interface StoryboardScene {
  scene_number: number;
  badge: string;
  title: string;
  subtitle: string;
  visual_prompt?: string;
  duration: number;
  audio_cue?: string;
}

export interface VideoAsset {
  filename: string;
  url: string;
  aspect_ratio: string;
  resolution: string;
  duration_seconds: number;
  fps: number;
  has_audio: boolean;
}

export interface PosterAsset {
  filename: string;
  url: string;
  dimensions: string;
}

export interface CarouselSlide {
  slide: number;
  title: string;
  bullet: string;
  tag: string;
}

export interface PlatformCaption {
  hook: string;
  caption: string;
  hashtags: string[];
  cta: string;
}

export interface GeneratedAssets {
  video?: VideoAsset;
  poster?: PosterAsset;
  videos?: VideoAsset[];
  posters?: PosterAsset[];
  carousel_slides?: CarouselSlide[];
  captions?: Record<string, PlatformCaption>;
}

export interface QualityCheckItem {
  name: string;
  status: 'PASS' | 'WARN';
  details: string;
}

export interface QualityReport {
  score: number;
  status: string;
  claims_verified: boolean;
  checks: QualityCheckItem[];
}

export interface PublishedPlatformPost {
  type: string;
  post_id: string;
  url: string;
  media_url?: string;
  status: string;
}

export interface PublishedRecord {
  platform: string;
  status: string;
  external_post_id?: string;
  post_url?: string;
  is_mock?: boolean;
  notes?: string;
  error_message?: string;
  posts?: PublishedPlatformPost[];
}

export interface CampaignStepLog {
  timestamp?: string;
  step: string;
  message: string;
}

export interface Campaign {
  id: number;
  title: string;
  prompt: string;
  product_ids: number[];
  brand_kit_id?: number;
  target_audience: string;
  tone: string;
  language: string;
  objective: string;
  cta: string;
  platforms: string[];
  video_format: string;
  poster_format: string;
  qc_retry_count?: number;
  formats?: string[];
  status: 'DRAFT' | 'IN_PROGRESS' | 'WAITING_APPROVAL' | 'APPROVED' | 'PUBLISHED' | 'FAILED';
  current_step: string;
  step_logs: CampaignStepLog[];
  product_analysis?: Record<string, any>;
  campaign_plan?: Record<string, any>;
  storyboard: StoryboardScene[];
  generated_assets: GeneratedAssets;
  quality_report?: QualityReport;
  published_records: PublishedRecord[];
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface PublishingAccount {
  id: number;
  platform: string;
  display_name: string;
  handle: string;
  avatar_url?: string;
  is_connected: boolean;
  is_mock: boolean;
  credentials_mask: string;
  account_metadata: Record<string, any>;
  updated_at: string;
}

export interface PublishingLog {
  id: number;
  campaign_id: number;
  platform: string;
  status: string;
  external_post_id?: string;
  post_url?: string;
  error_message?: string;
  scheduled_for?: string;
  published_at: string;
}

export interface AnalyticsOverview {
  products_count: number;
  total_campaigns: number;
  published_campaigns: number;
  waiting_approval: number;
  in_progress: number;
  connected_accounts: number;
  total_videos_rendered: number;
  average_qc_score: number;
  platform_distribution: Record<string, number>;
  estimated_reach_multiplier: string;
}
