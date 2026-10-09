from typing import TypedDict, List, Dict, Any, Optional

class MarketingWorkflowState(TypedDict, total=False):
    campaign_id: int
    product_ids: List[int]
    brand_kit_id: Optional[int]
    prompt: str
    target_audience: str
    tone: str
    language: str
    objective: str
    cta: str
    
    # Specific Platforms (Strictly Instagram, Facebook, YouTube)
    platforms: List[str]
    
    # Formats (Single video format, single poster format)
    video_format: str
    poster_format: str
    
    # State tracking
    status: str
    current_step: str
    step_logs: List[Dict[str, Any]]
    
    # Quality Control Checkpoint & Retry Loop
    qc_retry_count: int
    max_qc_retries: int
    qc_passed: bool
    qc_feedback: Optional[str]
    
    # Raw inputs fetched from DB
    product_data: Dict[str, Any]
    brand_kit: Dict[str, Any]
    
    # Workflow pipeline artifacts
    product_analysis: Dict[str, Any]
    campaign_plan: Dict[str, Any]
    storyboard: List[Dict[str, Any]]
    quality_report: Dict[str, Any]
    
    # Generated Media (Parallel generation branches)
    generated_poster: Optional[Dict[str, Any]]
    generated_video: Optional[Dict[str, Any]]
    generated_assets: Dict[str, Any]
    
    # Approval & Publishing
    approval_status: str  # PENDING | APPROVED | REJECTED
    published_records: List[Dict[str, Any]]
    
    error: Optional[str]
