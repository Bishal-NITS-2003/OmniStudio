# OmniPost AI — GenAI Social Media Marketing Automation Platform

An autonomous, full-stack, omnichannel social media marketing platform powered by **React + TypeScript + Vanilla CSS**, **Python + FastAPI**, and **LangChain + LangGraph**. 

OmniPost AI analyzes product catalogs, plans cohesive multi-scene campaign themes, generates platform-tailored social copy, and automatically renders polished product videos from images with transitions, text badges, and royalty-free background music.

---

## 🌟 Key Features

1. **Product Inventory & Smart Importer**
   - CRUD management for products (prices, descriptions, categories, features, image galleries).
   - Instant import from **Amazon**, **Flipkart**, and e-commerce URLs with an automated extraction engine and an interactive human verification modal before catalog saving.
   - Local image upload and preview gallery.

2. **Brand Kit & Creative System**
   - Custom brand palette (Primary, Secondary, Accent, Dark Theme background) with live color pickers.
   - Typography and voice guidelines (Energetic, Luxury, Minimalist, Bold, etc.).
   - Reusable creative rules and target customer persona.

3. **Multi-Format AI Campaign Builder**
   - Natural language campaign prompt with prompt inspiration chips.
   - Multi-format generation in a single run:
     - **9:16 Vertical Video** (Instagram Reels, TikTok, YouTube Shorts)
     - **16:9 Landscape Video** (YouTube, LinkedIn)
     - **1:1 Square Feed Post** (Instagram, Facebook)
     - **Swipeable Carousel Cards**
     - **Platform Captions & Optimized Hashtags**

4. **Product Video Generation with Transitions & Audio**
   - Assembles multiple product images with smooth crossfade and zoom motion.
   - Overlays high-contrast product badges, titles, and subtitles.
   - Synthesizes and mixes royalty-free procedural musical backing tracks (Upbeat, Lo-fi, Ambient) in pure Python.
   - Encodes web-ready H.264 + AAC MP4 video files via FFmpeg (`imageio-ffmpeg`).

5. **LangGraph Autonomous Workflow**
   - Structured 7-node pipeline:
     1. `analyze_product`: Extracts USPs, value props, and target persona.
     2. `plan_campaign`: Crafts creative theme and scene-by-scene storyboard.
     3. `generate_content`: Generates platform-specific social copy and carousel slides.
     4. `assemble_media`: Compiles promotional posters and transition product videos.
     5. `quality_check`: Audits claim truthfulness, duration, text contrast, and platform policies.
     6. `human_approval`: Resumable checkpoint gate for user sign-off.
     7. `publish_content`: Dispatches to connected channels or saves to download vault.

6. **Social Media Publishing & Demo Sandbox**
   - Official API adapters for Instagram, LinkedIn, TikTok, and YouTube Shorts.
   - Dual-mode architecture: runs in **Demo Sandbox Mode** out-of-the-box (zero paid credentials needed) or seamlessly switches to live OAuth tokens.
   - Full ZIP export download center containing all rendered MP4s, posters, caption text files, and storyboard plans.

---

## 🏗️ Architecture & Tech Stack

```
gen-ai/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI routers (products, brand_kit, campaigns, publishing, analytics)
│   │   ├── core/            # Configuration (pydantic-settings), database engine
│   │   ├── models/          # SQLAlchemy ORM models (SQLite / PostgreSQL)
│   │   ├── schemas/         # Pydantic v2 schemas
│   │   ├── services/        # Product importer, AI providers, video engine, audio synth, publishers
│   │   ├── workflows/       # LangGraph state schema, nodes, and compiled StateGraph
│   │   ├── main.py          # FastAPI application entrypoint & static media mount
│   │   └── seed_data.py     # Default catalog items and demo campaign
│   ├── storage/             # Generated videos, posters, audio tracks, and uploads
│   ├── tests/               # Pytest suite for APIs and LangGraph workflows
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/             # REST API client
    │   ├── components/      # VideoPlayer, StepperProgress, QualityCheckCard, Modal, Toast
    │   ├── views/           # Dashboard, Products, CampaignBuilder, CampaignDetail, BrandKit, Publishing
    │   ├── types/           # TypeScript interfaces
    │   ├── index.css        # Vanilla CSS design system (glassmorphism & dark theme)
    │   └── App.tsx          # Main application & routing
    └── package.json
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Node.js 18+ (tested on Node v22)

---

### Step 1: Run Backend

1. Navigate to the backend directory and activate the virtual environment:
   ```powershell
   cd backend
   .\venv\Scripts\activate
   ```

2. (Optional) Configure environment variables in `.env`:
   ```bash
   cp .env.example .env
   ```
   *Note: OmniPost AI operates completely in Demo Mode without requiring any external paid API keys!*

3. Launch the FastAPI server:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
   Backend will start at `http://127.0.0.1:8000`. Interactive Swagger API docs are available at `http://127.0.0.1:8000/docs`.

---

### Step 2: Run Frontend

1. In a separate terminal, navigate to the frontend directory:
   ```powershell
   cd frontend
   npm run dev
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

---

## 🧪 Running Automated Tests

Run backend integration and LangGraph pipeline tests:
```powershell
cd backend
.\venv\Scripts\pytest backend\tests\
```

All tests validate:
- System health check & CRUD operations
- URL extraction heuristics (Amazon / Flipkart)
- End-to-end LangGraph state transition and node execution
- Video rendering and audio muxing pipeline

---

## ⚙️ Configuration Reference

| Environment Variable | Default | Purpose |
| -------------------- | ------- | ------- |
| `DATABASE_URL` | `sqlite:///./social_marketing.db` | SQLAlchemy connection string (SQLite or PostgreSQL) |
| `DEMO_MODE` | `True` | Runs in sandbox mode with zero paid API requirements |
| `GEMINI_API_KEY` | *(optional)* | Google Gemini LLM API key |
| `GROQ_API_KEY` | *(optional)* | Groq API key for alternative high-speed inference |
| `META_ACCESS_TOKEN` | *(optional)* | Instagram/Facebook Graph API access token |
| `LINKEDIN_ACCESS_TOKEN` | *(optional)* | LinkedIn Community API access token |

---

## 📄 License
MIT License. Built with ❤️ by the OmniPost AI team.
