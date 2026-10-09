import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# Core LangChain Concepts
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.output_parsers import (
    PydanticOutputParser,
    JsonOutputParser
)
from langchain_core.documents import Document

from app.core.config import settings

# ---------------------------------------------------------------------------
# Structured Output Pydantic Schemas (LangChain Structured Output)
# ---------------------------------------------------------------------------

class ProductAnalysisOutput(BaseModel):
    product_name: str = Field(description="Name of the analyzed product")
    category: str = Field(description="Market category of the product")
    price_tag: str = Field(description="Formatted price string")
    core_value_prop: str = Field(description="Main value proposition hook")
    target_persona: str = Field(description="Description of target buyer persona")
    emotional_hooks: List[str] = Field(description="Emotional triggers and scroll-stopping hooks")
    key_usps: List[str] = Field(description="Key unique selling propositions")
    competitive_edge: str = Field(description="Competitive differentiation angle")

class StoryboardSceneModel(BaseModel):
    scene_number: int = Field(description="Sequence number of the scene")
    badge: str = Field(description="High-contrast top badge text like INTRODUCING or LIMITED OFFER")
    title: str = Field(description="Main bold headline text for the scene")
    subtitle: str = Field(description="Secondary descriptive subtitle")
    visual_prompt: str = Field(description="Visual description for scene transition and imagery")
    duration: float = Field(default=3.0, description="Duration of this scene in seconds")
    audio_cue: Optional[str] = Field(default=None, description="Audio mood cue")

class CampaignPlanOutput(BaseModel):
    creative_theme: str = Field(description="Overarching creative concept theme")
    narrative_arc: str = Field(description="Narrative progression structure")
    campaign_objective: str = Field(description="Primary campaign objective")
    tone_selected: str = Field(description="Brand voice tone applied")
    storyboard: List[StoryboardSceneModel] = Field(description="Scene by scene storyboard outline")
    total_estimated_duration: float = Field(default=12.0, description="Total video duration in seconds")

class PlatformCopyModel(BaseModel):
    hook: str = Field(description="Scroll stopping opening hook line")
    caption: str = Field(description="Full formatted post caption with spacing and emojis")
    hashtags: List[str] = Field(description="List of relevant hashtags")
    cta: str = Field(description="Specific call to action")

class CarouselSlideModel(BaseModel):
    slide: int = Field(description="Slide sequence number")
    title: str = Field(description="Bold headline on the card")
    bullet: str = Field(description="Concise value bullet point")
    tag: str = Field(description="Small accent badge or navigation pill")

class SocialContentOutput(BaseModel):
    captions: Dict[str, PlatformCopyModel] = Field(description="Captions mapped by platform key: instagram, linkedin, tiktok, youtube")
    carousel_slides: List[CarouselSlideModel] = Field(description="Multi-card carousel sequence")

class QualityCheckItemModel(BaseModel):
    name: str = Field(description="Name of the validation check")
    status: str = Field(description="PASS or WARN")
    details: str = Field(description="Explanation of check result")

class QualityReportOutput(BaseModel):
    score: int = Field(ge=0, le=100, description="Overall compliance and quality score from 0 to 100")
    status: str = Field(description="PASSED or WARNING")
    claims_verified: bool = Field(description="Whether marketing claims match product specs")
    aspect_ratios_checked: bool = Field(default=True, description="Aspect ratio conformity check")
    audio_sync_checked: bool = Field(default=True, description="Audio track sync check")
    checks: List[QualityCheckItemModel] = Field(description="Individual audit checklist items")

# ---------------------------------------------------------------------------
# Custom LangChain Chat Model for Offline / Demo Mode
# ---------------------------------------------------------------------------

class MockLangChainChatModel(BaseChatModel):
    """
    Custom LangChain Chat Model implementing BaseChatModel.
    Ensures that LangChain LCEL chains (prompt | llm | output_parser) execute
    fully through LangChain interfaces even without paid third-party API keys.
    """

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        full_text = " ".join([m.content for m in messages if isinstance(m.content, str)])

        if "social" in full_text.lower() or "copywriter" in full_text.lower() or "carousel" in full_text.lower() or "captions" in full_text.lower():
            response_dict = {
                "captions": {
                    "instagram": {
                        "hook": "Stop scrolling. This changes everything ✨",
                        "caption": "Stop scrolling. This changes everything ✨\n\nMeet your new everyday essential. Engineered for high performance, maximum comfort, and timeless aesthetic.\n\n🔥 Launch perk: First 50 orders get free expedited priority delivery!\n\n👉 Tap link in bio to claim yours.",
                        "hashtags": ["#ProductDrop", "#TechInnovation", "#SmartLifestyle", "#DesignInspo", "#MustHave2026"],
                        "cta": "Link in Bio"
                    },
                    "facebook": {
                        "hook": "Upgrade your setup today with unmatched performance 🚀",
                        "caption": "Upgrade your setup today with unmatched performance 🚀\n\nEngineered for seamless daily use and top-tier reliability. Get yours today with exclusive launch benefits and free shipping across India!\n\n👉 Click Shop Now to order.",
                        "hashtags": ["#ProductLaunch", "#BestDeals", "#Innovation", "#MustHave"],
                        "cta": "Shop Now"
                    },
                    "youtube": {
                        "hook": "Is It Actually Worth The Hype? First Look & Breakdown",
                        "caption": "Is this release actually worth the hype? In this quick breakdown, we take a look at the design, performance, and key highlights.\n\n🔔 Subscribe for weekly reviews, product drops, and tech breakdowns.\n\n🛒 Exclusive purchase link in description & pinned comment.",
                        "hashtags": ["#Shorts", "#ProductReview", "#Trending", "#TechShorts"],
                        "cta": "Watch & Shop"
                    }
                },
                "carousel_slides": [
                    {
                        "slide": 1,
                        "title": "Why Everyone Is Talking About It",
                        "bullet": "The breakthrough release of the season",
                        "tag": "SWIPE ➡️"
                    },
                    {
                        "slide": 2,
                        "title": "Built For High Performance",
                        "bullet": "Premium materials engineered for longevity",
                        "tag": "FEATURE 01"
                    },
                    {
                        "slide": 3,
                        "title": "Designed For Your Lifestyle",
                        "bullet": "Seamless integration into your work and play",
                        "tag": "FEATURE 02"
                    },
                    {
                        "slide": 4,
                        "title": "Claim Yours With Launch Perks",
                        "bullet": "Available now with 30-day money back guarantee",
                        "tag": "ORDER NOW"
                    }
                ]
            }
        elif "compliance" in full_text.lower() or "standards" in full_text.lower() or "audit" in full_text.lower():
            response_dict = {
                "score": 96,
                "status": "PASSED",
                "claims_verified": True,
                "aspect_ratios_checked": True,
                "audio_sync_checked": True,
                "checks": [
                    {"name": "Product Claim Truthfulness", "status": "PASS", "details": "All generated copy matches verified specifications with zero fabricated claims."},
                    {"name": "Social Aspect Ratio Compliance", "status": "PASS", "details": "Generated formats match 9:16 vertical and 1:1 feed square standards."},
                    {"name": "Text & Subtitle Legibility", "status": "PASS", "details": "High-contrast text badges with darkened gradient vignette backdrops."},
                    {"name": "Brand Safety & Platform Policy", "status": "PASS", "details": "No banned hashtags or spam patterns detected."}
                ]
            }
        elif "advertising director" in full_text.lower() or "creative theme" in full_text.lower():
            response_dict = {
                "creative_theme": "Unlock Next-Level Standards",
                "narrative_arc": "Attention Hook -> Core Value Proposition -> Proof of Quality -> Direct Call-to-Action",
                "campaign_objective": "Conversions & Brand Awareness",
                "tone_selected": "Energetic & Modern",
                "storyboard": [
                    {
                        "scene_number": 1,
                        "badge": "INTRODUCING",
                        "title": "Next-Gen Innovation",
                        "subtitle": "Redefining everyday performance",
                        "visual_prompt": "Cinematic close-up showcase of the product under sleek studio lighting",
                        "duration": 3.0,
                        "audio_cue": "Upbeat synth swell with clear rhythmic bass"
                    },
                    {
                        "scene_number": 2,
                        "badge": "SUPERIOR SPECS",
                        "title": "Built Without Compromise",
                        "subtitle": "Precision engineering meets ultra comfort",
                        "visual_prompt": "Dynamic angle highlighting key features and high-grade build quality",
                        "duration": 3.0,
                        "audio_cue": "Driving rhythm and energetic cadence"
                    },
                    {
                        "scene_number": 3,
                        "badge": "UNMATCHED QUALITY",
                        "title": "Crafted For You",
                        "subtitle": "Tested and loved by creators worldwide",
                        "visual_prompt": "Lifestyle in-use context demonstrating real-world satisfaction",
                        "duration": 3.0,
                        "audio_cue": "High-energy bridge with ambient clarity"
                    },
                    {
                        "scene_number": 4,
                        "badge": "LIMITED TIME",
                        "title": "Claim Yours Today",
                        "subtitle": "Exclusive discount available for early adopters",
                        "visual_prompt": "Final bold call-to-action screen with brand logo and limited-time offer badge",
                        "duration": 3.0,
                        "audio_cue": "Memorable audio resolution and logo sting"
                    }
                ],
                "total_estimated_duration": 12.0
            }
        else:
            response_dict = {
                "product_name": "Premium Feature Product",
                "category": "Consumer Lifestyle & Tech",
                "price_tag": "$99.00",
                "core_value_prop": "Elevating everyday performance through smart design and uncompromising craft.",
                "target_persona": "Value-conscious modern innovators and trendsetters looking for premium functionality.",
                "emotional_hooks": [
                    "The upgrade you didn't know you needed, but won't live without",
                    "Crafted for those who refuse to compromise on design or utility",
                    "Instant game changer for your daily routine"
                ],
                "key_usps": [
                    "Precision engineered for peak daily performance",
                    "Sleek ergonomic design crafted from premium materials",
                    "Backed by a 100% satisfaction guarantee"
                ],
            }

        generation = ChatGeneration(message=AIMessage(content=json.dumps(response_dict)))
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock-langchain-chat-model"

# ---------------------------------------------------------------------------
# LangChain Orchestrated AI Service Interface
# ---------------------------------------------------------------------------

class LangChainMarketingIntelligence:
    """
    Marketing intelligence orchestrator built entirely on LangChain concepts:
    - Chat Models (ChatGoogleGenerativeAI, ChatGroq, MockLangChainChatModel)
    - ChatPromptTemplate, PromptTemplate, MessagesPlaceholder, SystemMessage, HumanMessage
    - Structured Output with PydanticOutputParser and JsonOutputParser
    - Document abstraction for catalog item representations
    """

    def __init__(self, chat_model: BaseChatModel):
        self.llm = chat_model

    def analyze_product(self, product_data: Dict[str, Any], prompt: str) -> Dict[str, Any]:
        """
        Uses LangChain ChatPromptTemplate + PydanticOutputParser to extract
        structured product analysis.
        """
        parser = PydanticOutputParser(pydantic_object=ProductAnalysisOutput)

        # Convert product dictionary into LangChain Document representation i.e page_content and metadata
        product_doc = Document(
            page_content=f"Product: {product_data.get('name', '')}\n"
                         f"Description: {product_data.get('description', '')}\n"
                         f"Features: {', '.join(product_data.get('features', []))}\n"
                         f"Price: {product_data.get('currency', '$')}{product_data.get('price', 0)}",
            metadata={"category": product_data.get("category", "General"), "source": product_data.get("source_url", "")}
        )

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are an elite product marketing strategist and brand positioning expert.\n"
                "Your role is to deeply analyze products and formulate high-converting marketing hooks.\n"
                "{format_instructions}"    #Placeholder that is filled when the chain is executed
            )),
            HumanMessage(content=(
                "Here is the product document to analyze:\n"
                "----------------------------------------\n"
                "{product_content}\n"      #Placeholder that is filled when the chain is executed
                "----------------------------------------\n\n"
                "Campaign Objective / User Goal: {user_goal}\n"
                "Extract positioning, target persona, emotional hooks, and core USPs."
            ))
        ])

        # LCEL Chain: prompt | llm | parser
        chain = chat_prompt | self.llm | parser

        try:
            result: ProductAnalysisOutput = chain.invoke({
                "format_instructions": parser.get_format_instructions(),
                "product_content": product_doc.page_content,
                "user_goal": prompt
            })
            return result.model_dump()
        except Exception:
            # Fallback to direct model invocation if parser needs raw JSON dict
            json_parser = JsonOutputParser()
            fallback_chain = chat_prompt | self.llm | json_parser
            return fallback_chain.invoke({
                "format_instructions": json_parser.get_format_instructions(),
                "product_content": product_doc.page_content,
                "user_goal": prompt
            })

    def plan_campaign(self, analysis: Dict[str, Any], campaign_meta: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uses LangChain ChatPromptTemplate + PydanticOutputParser to plan
        campaign narrative arc and multi-scene storyboard.
        """
        parser = PydanticOutputParser(pydantic_object=CampaignPlanOutput)

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are an award-winning creative advertising director.\n"
                "Create a multi-scene storyboard that captures attention within 2 seconds "
                "and delivers a clear visual call-to-action.\n"
                "{format_instructions}"
            )),
            HumanMessage(content=(
                "Product Positioning Analysis: {analysis_json}\n"
                "Campaign Settings: {campaign_meta_json}\n\n"
                "Design a cohesive creative theme, narrative arc, and 3-5 scene storyboard "
                "with badges, headlines, subtitles, and durations."
            ))
        ])

        chain = chat_prompt | self.llm | parser

        try:
            result: CampaignPlanOutput = chain.invoke({
                "format_instructions": parser.get_format_instructions(),
                "analysis_json": json.dumps(analysis),
                "campaign_meta_json": json.dumps(campaign_meta)
            })
            return result.model_dump()  # converts a data model instance (Pydantic Object) to a standard Python dictionary
        except Exception:
            json_parser = JsonOutputParser()
            fallback_chain = chat_prompt | self.llm | json_parser
            return fallback_chain.invoke({
                "format_instructions": json_parser.get_format_instructions(),
                "analysis_json": json.dumps(analysis),
                "campaign_meta_json": json.dumps(campaign_meta)
            })

    def generate_social_content(
        self,
        campaign_plan: Dict[str, Any],
        platforms: List[str],
        brand_kit: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Uses LangChain ChatPromptTemplate + Structured Output to generate
        multi-platform captions, hashtags, and carousel slides in parallel.
        """
        parser = PydanticOutputParser(pydantic_object=SocialContentOutput)

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are a viral social media strategist and expert copywriter.\n"
                "Craft platform-native copy: punchy hooks for Instagram/TikTok, thought leadership for LinkedIn, "
                "and informative descriptions for YouTube Shorts.\n"
                "{format_instructions}"
            )),
            HumanMessage(content=(
                "Campaign Plan & Storyboard: {plan_json}\n"
                "Target Platforms: {platforms}\n"
                "Brand Guidelines: {brand_kit_json}\n\n"
                "Generate platform-specific captions with hashtags and a 4-card carousel outline."
            ))
        ])

        chain = chat_prompt | self.llm | parser

        try:
            result: SocialContentOutput = chain.invoke({
                "format_instructions": parser.get_format_instructions(),
                "plan_json": json.dumps(campaign_plan),
                "platforms": ", ".join(platforms),
                "brand_kit_json": json.dumps(brand_kit or {})
            })
            return result.model_dump()
        except Exception:
            json_parser = JsonOutputParser()
            fallback_chain = chat_prompt | self.llm | json_parser
            return fallback_chain.invoke({
                "format_instructions": json_parser.get_format_instructions(),
                "plan_json": json.dumps(campaign_plan),
                "platforms": ", ".join(platforms),
                "brand_kit_json": json.dumps(brand_kit or {})
            })

    def evaluate_quality(
        self,
        campaign_data: Dict[str, Any],
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Uses LangChain ChatPromptTemplate + PydanticOutputParser to audit marketing
        claims against actual product specifications for safety and compliance.
        """
        parser = PydanticOutputParser(pydantic_object=QualityReportOutput)

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are a strict advertising standards and compliance auditor.\n"
                "Verify that marketing copy accurately reflects product specifications with "
                "zero fabricated warranties or false technical claims.\n"
                "{format_instructions}"
            )),
            HumanMessage(content=(
                "Campaign Materials: {campaign_json}\n"
                "Source Product Specifications: {product_json}\n\n"
                "Audit product claim truthfulness, duration, aspect ratio compatibility, and text contrast. "
                "Score from 0 to 100."
            ))
        ])

        chain = chat_prompt | self.llm | parser

        try:
            result: QualityReportOutput = chain.invoke({
                "format_instructions": parser.get_format_instructions(),
                "campaign_json": json.dumps(campaign_data),
                "product_json": json.dumps(product_data)
            })
            return result.model_dump()
        except Exception:
            json_parser = JsonOutputParser()
            fallback_chain = chat_prompt | self.llm | json_parser
            return fallback_chain.invoke({
                "format_instructions": json_parser.get_format_instructions(),
                "campaign_json": json.dumps(campaign_data),
                "product_json": json.dumps(product_data)
            })

# ---------------------------------------------------------------------------
# Factory: Initialize LangChain Chat Model
# ---------------------------------------------------------------------------

def get_chat_model() -> BaseChatModel:
    """
    Returns an initialized LangChain ChatModel:
    - ChatGoogleGenerativeAI if GEMINI_API_KEY is configured
    - ChatGroq if GROQ_API_KEY is configured
    - MockLangChainChatModel if running in Demo Sandbox mode
    """
    if settings.GEMINI_API_KEY and not settings.DEMO_MODE:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.7
            )
        except Exception:
            pass

    if settings.GROQ_API_KEY and not settings.DEMO_MODE:
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                model_name="llama-3.3-70b-versatile",
                groq_api_key=settings.GROQ_API_KEY,
                temperature=0.7
            )
        except Exception:
            pass

    return MockLangChainChatModel()

def get_ai_provider() -> LangChainMarketingIntelligence:
    """Returns the unified LangChain marketing intelligence provider."""
    chat_model = get_chat_model()
    return LangChainMarketingIntelligence(chat_model)
