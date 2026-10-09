from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.brand_kit import BrandKit
from app.models.campaign import Campaign
from app.models.publishing import PublishingAccount

def seed_database(db: Session):
    # 1. Seed Products if empty
    if db.query(Product).count() == 0:
        products = [
            Product(
                name="AeroPulse Wireless ANC Headphones",
                tagline="Immersive Sound, 40-Hour Playtime, Ultra Comfort",
                description="Engineered with custom 40mm titanium dynamic drivers and hybrid active noise cancellation up to 45dB. Features ultra-breathable protein leather memory foam ear cups and instant multi-device switching.",
                category="Audio & Electronics",
                price=7999.00,
                currency="Rs.",
                brand_name="AeroPulse Labs",
                features=[
                    "45dB Hybrid Active Noise Cancellation",
                    "40-Hour Battery with 10-Minute Fast Charge",
                    "Hi-Res Audio Certified with Spatial Acoustic Profiling",
                    "Multipoint Bluetooth 5.3 Connection"
                ],
                image_urls=[
                    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",
                    "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&q=80",
                    "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80"
                ],
                tags=["ANC", "Wireless", "Audio", "Gen-Z", "Gaming"],
                source_url="https://www.amazon.in/dp/B09EXAMPLE"
            ),
            Product(
                name="NovaGlow Triple Vitamin C Brightening Serum",
                tagline="Clinical Radiance with 15% Ethyl Ascorbic & Hyaluronic Complex",
                description="A fast-absorbing, dermatologically validated elixir formulated with 15% stabilized vitamin C, ferulic acid, and botanical botanicals. Targets dullness, protects against oxidative stress, and evens skin tone in 14 days.",
                category="Beauty & Skincare",
                price=1499.00,
                currency="Rs.",
                brand_name="NovaGlow Botanicals",
                features=[
                    "15% Stabilized Triple Vitamin C + Ferulic Acid",
                    "Multi-molecular Hyaluronic Acid for Deep Hydration",
                    "100% Vegan, Fragrance-Free & Cruelty-Free",
                    "Clinical Proven 28% Brightness Increase in 2 Weeks"
                ],
                image_urls=[
                    "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=80",
                    "https://images.unsplash.com/photo-1608248597359-00994f3879f9?w=800&q=80"
                ],
                tags=["Skincare", "Vitamin C", "Clean Beauty", "Anti-Aging"],
                source_url="https://www.nykaa.com/product/example-serum"
            ),
            Product(
                name="Chronos Apex Titanium Smartwatch",
                tagline="Grade 5 Titanium Bezel with Sapphire AMOLED & Bio-Telemetry",
                description="Designed for high-performance athletes and busy professionals. Aerospace titanium body with 1.43-inch always-on AMOLED display, VO2 max estimation, ECG monitoring, and 14-day extended battery life.",
                category="Wearables & Fitness",
                price=14999.00,
                currency="Rs.",
                brand_name="Chronos Precision",
                features=[
                    "Grade 5 Aerospace Titanium Bezel",
                    "1.43-inch Always-on AMOLED (1,000 Nits Outdoor)",
                    "Dual-Frequency Multi-GNSS GPS Navigation",
                    "14-Day Battery Life & 50m Water Resistance"
                ],
                image_urls=[
                    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80",
                    "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=80"
                ],
                tags=["Smartwatch", "Titanium", "Fitness", "Luxury", "Outdoor"],
                source_url="https://www.amazon.in/dp/B08EXAMPLE"
            )
        ]
        db.add_all(products)
        db.commit()

    # 2. Seed Brand Kit if empty
    brand = db.query(BrandKit).first()
    if not brand:
        brand = BrandKit(
            name="OmniNova Studio",
            logo_url="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200&q=80",
            primary_color="#6366f1",
            secondary_color="#ec4899",
            accent_color="#06b6d4",
            background_color="#0f172a",
            font_family="Inter",
            tone_of_voice="Energetic & Modern",
            target_persona="Tech-forward buyers and creative professionals looking for premium performance.",
            guidelines=[
                "High contrast text with rounded badge pill accents",
                "Hook viewers within the first 2 seconds of video",
                "Ensure call-to-action is prominent and clear"
            ]
        )
        db.add(brand)
        db.commit()
        db.refresh(brand)

    # 3. Seed an initial Demo Campaign if none exist
    if db.query(Campaign).count() == 0:
        p1 = db.query(Product).first()
        demo_campaign = Campaign(
            title="Summer Soundwave Flash Sale",
            prompt="Launch an energetic flash sale targeting Gen-Z music lovers and fitness enthusiasts for summer. Emphasize noise cancellation and 40-hr battery.",
            product_ids=[p1.id] if p1 else [],
            brand_kit_id=brand.id,
            target_audience="Music lovers, gym enthusiasts, and remote workers (18-34)",
            tone="Energetic & Modern",
            language="English",
            objective="Conversions & Brand Awareness",
            cta="Shop Now (30% Off)",
            platforms=["instagram", "facebook", "youtube"],
            video_format="9:16",
            poster_format="1:1",
            qc_retry_count=0,
            status="WAITING_APPROVAL",
            current_step="human_approval",
            step_logs=[
                {"timestamp": "2026-10-09T08:00:00Z", "step": "analyze_product", "message": "Extracted key USPs: 45dB ANC and 40h battery."},
                {"timestamp": "2026-10-09T08:00:03Z", "step": "plan_campaign", "message": "Planned 4-scene narrative arc targeting active summer lifestyle."},
                {"timestamp": "2026-10-09T08:00:08Z", "step": "generate_content", "message": "Generated platform-specific captions and storyboard."},
                {"timestamp": "2026-10-09T08:00:12Z", "step": "quality_check", "message": "Pre-generation QC passed with 96/100 quality score (0 retries)."},
                {"timestamp": "2026-10-09T08:00:15Z", "step": "generate_poster", "message": "Generated promotional poster in 1:1 format."},
                {"timestamp": "2026-10-09T08:00:18Z", "step": "generate_video", "message": "Assembled branded 9:16 video with dynamic slides and BGM."},
                {"timestamp": "2026-10-09T08:00:20Z", "step": "human_approval", "message": "Pipeline paused at human review gate. Ready for one-click approval."}
            ],
            product_analysis={
                "product_name": "AeroPulse Wireless ANC Headphones",
                "core_value_prop": "Studio-grade silence anywhere with 45dB hybrid ANC and ultra-comfort design.",
                "target_persona": "College students, daily commuters, and fitness lovers seeking uninterrupted focus.",
                "key_usps": [
                    "45dB Hybrid Active Noise Cancellation",
                    "40-Hour Battery with 10-Min Fast Charge",
                    "Hi-Res Audio Certified with Spatial Profiling"
                ]
            },
            campaign_plan={
                "creative_theme": "Zone Out the World. Zone Into Summer.",
                "narrative_arc": "Problem (Chaos/Noise) -> Solution (AeroPulse ANC) -> Feature Highlights -> Limited Time CTA",
                "storyboard": [
                    {"scene_number": 1, "badge": "SUMMER DROP", "title": "AeroPulse Pro ANC", "subtitle": "Silence the Noise. Amplify Summer.", "duration": 3.0},
                    {"scene_number": 2, "badge": "45dB HYBRID ANC", "title": "Pure Acoustic Immersion", "subtitle": "Block Out Distractions Instantly", "duration": 3.0},
                    {"scene_number": 3, "badge": "40H PLAYTIME", "title": "Sound That Doesn't Stop", "subtitle": "Quick 10-Min Charge = 5 Hours", "duration": 3.0},
                    {"scene_number": 4, "badge": "LIMITED OFFER", "title": "Get 30% Off Today", "subtitle": "Tap Below to Claim Launch Perks", "duration": 3.0}
                ]
            },
            storyboard=[
                {"scene_number": 1, "badge": "SUMMER DROP", "title": "AeroPulse Pro ANC", "subtitle": "Silence the Noise. Amplify Summer.", "duration": 3.0},
                {"scene_number": 2, "badge": "45dB HYBRID ANC", "title": "Pure Acoustic Immersion", "subtitle": "Block Out Distractions Instantly", "duration": 3.0},
                {"scene_number": 3, "badge": "40H PLAYTIME", "title": "Sound That Doesn't Stop", "subtitle": "Quick 10-Min Charge = 5 Hours", "duration": 3.0},
                {"scene_number": 4, "badge": "LIMITED OFFER", "title": "Get 30% Off Today", "subtitle": "Tap Below to Claim Launch Perks", "duration": 3.0}
            ],
            generated_assets={
                "video": {
                    "filename": "demo_video.mp4",
                    "url": "https://assets.mixkit.co/videos/preview/mixkit-headphones-lying-on-a-table-41484-large.mp4",
                    "aspect_ratio": "9:16",
                    "resolution": "720x1280",
                    "duration_seconds": 12.0,
                    "fps": 24,
                    "has_audio": True
                },
                "poster": {
                    "filename": "demo_poster.jpg",
                    "url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",
                    "aspect_ratio": "1:1",
                    "dimensions": "1080x1080"
                },
                "videos": [
                    {
                        "filename": "demo_video.mp4",
                        "url": "https://assets.mixkit.co/videos/preview/mixkit-headphones-lying-on-a-table-41484-large.mp4",
                        "aspect_ratio": "9:16",
                        "resolution": "720x1280",
                        "duration_seconds": 12.0,
                        "fps": 24,
                        "has_audio": True
                    }
                ],
                "posters": [
                    {
                        "filename": "demo_poster.jpg",
                        "url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",
                        "dimensions": "1080x1080"
                    }
                ],
                "captions": {
                    "instagram": {
                        "hook": "Your daily commute will never sound the same again 🎧⚡",
                        "caption": "Your daily commute will never sound the same again 🎧⚡\n\nMeet the AeroPulse ANC Headphones. Engineered with 45dB hybrid noise cancelation and titanium acoustic drivers, it turns any noisy cafe, train, or gym into your personal private studio.\n\n✨ 40-hour battery life\n✨ Ultra-breathable memory foam cushions\n✨ Fast 10-min charge gives 5 hours\n\n🔥 Summer Flash Sale is LIVE! Tap the link in our bio to get 30% off before stock runs out.",
                        "hashtags": ["#AeroPulse", "#Headphones", "#ANC", "#SummerDrop", "#TechFinds", "#MusicLifestyle"],
                        "cta": "Link in Bio"
                    },
                    "facebook": {
                        "hook": "Experience studio acoustics anywhere without breaking the bank 🎵",
                        "caption": "Experience studio acoustics anywhere without breaking the bank! 🎵\n\nThe AeroPulse ANC Headphones feature 45dB active noise cancellation and an incredible 40-hour battery life. Perfect for work, travel, and workouts.\n\nOrder today and get free express delivery across India! Limited stock available.",
                        "hashtags": ["#AeroPulseAudio", "#NoiseCancellation", "#DealsIndia", "#AudioLife"],
                        "cta": "Shop Now"
                    },
                    "youtube": {
                        "hook": "Is this the best budget ANC headphone in 2026? 🎧",
                        "caption": "Testing the AeroPulse ANC Headphones with 45dB Hybrid Noise Cancellation and 40H battery! Check out our full impressions and grab the limited launch discount in the description.",
                        "hashtags": ["#Shorts", "#TechReview", "#AeroPulse", "#ANCHeadphones"],
                        "cta": "Check Description"
                    }
                }
            },
            quality_report={
                "score": 96,
                "status": "PASSED",
                "claims_verified": True,
                "checks": [
                    {"name": "Product Claim Truthfulness", "status": "PASS", "details": "45dB ANC and 40h battery verified against product spec sheets."},
                    {"name": "Social Aspect Ratio Compliance", "status": "PASS", "details": "9:16 vertical and 1:1 square assets adhere to platform standards."},
                    {"name": "Text & Subtitle Legibility", "status": "PASS", "details": "High-contrast text badges with darkened gradient overlays."},
                    {"name": "Brand Safety & Platform Policy", "status": "PASS", "details": "Zero prohibited claims or spam triggers."}
                ]
            }
        )
        db.add(demo_campaign)
        db.commit()
