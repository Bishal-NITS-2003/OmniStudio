import concurrent.futures
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from app.workflows.state import MarketingWorkflowState
from app.workflows.nodes import (
    node_analyze_product,
    node_plan_campaign,
    node_generate_content,
    node_quality_check,
    node_generate_poster,
    node_generate_video,
    node_combine_media,
    node_human_approval,
    node_publish_parallel
)

def route_after_qc(state: MarketingWorkflowState) -> Literal["generate_poster", "generate_content"]:
    """Conditional router: loop back to generate_content if QC failed, else proceed to media generation."""
    if state.get("qc_passed", False):
        return "generate_poster"
    return "generate_content"

def route_after_approval(state: MarketingWorkflowState) -> Literal["publish_parallel", "__end__"]:
    """Conditional router based on human approval gate."""
    if state.get("approval_status") == "APPROVED":
        return "publish_parallel"
    return END

def build_marketing_graph():
    builder = StateGraph(MarketingWorkflowState)

    # Register Nodes
    builder.add_node("analyze_product", node_analyze_product)
    builder.add_node("plan_campaign", node_plan_campaign)
    builder.add_node("generate_content", node_generate_content)
    builder.add_node("quality_check", node_quality_check)
    builder.add_node("generate_poster", node_generate_poster)
    builder.add_node("generate_video", node_generate_video)
    builder.add_node("combine_media", node_combine_media)
    builder.add_node("human_approval", node_human_approval)
    builder.add_node("publish_parallel", node_publish_parallel)

    # Sequential edges up to QC
    builder.add_edge(START, "analyze_product")
    builder.add_edge("analyze_product", "plan_campaign")
    builder.add_edge("plan_campaign", "generate_content")
    builder.add_edge("generate_content", "quality_check")

    # QC Conditional Loop: If not passed, loop back to generate_content; else generate media
    builder.add_conditional_edges("quality_check", route_after_qc, ["generate_poster", "generate_content"])

    # Parallel Media Generation: poster and video both join into combine_media
    builder.add_edge("generate_poster", "combine_media")
    builder.add_edge("generate_video", "combine_media")
    builder.add_edge("combine_media", "human_approval")

    # Approval Gate: if approved -> publish_parallel -> END
    builder.add_conditional_edges("human_approval", route_after_approval, ["publish_parallel", END])
    builder.add_edge("publish_parallel", END)

    return builder.compile()

marketing_workflow_app = build_marketing_graph()

def run_campaign_workflow(initial_state: MarketingWorkflowState, db_updater=None) -> Dict[str, Any]:
    """
    Executes the workflow:
    1. Product Analysis
    2. Campaign Plan & Storyboard
    3. Multi-format Content Generation
    4. Quality Check with iterative retry loop before any media generation!
    5. Parallel Poster Generation & Video Generation (using concurrent threads)
    6. Combine Media
    7. Human Approval Checkpoint
    """
    current_state = dict(initial_state)

    # Step 1: Analyze Product
    out_analysis = node_analyze_product(current_state)
    current_state.update(out_analysis)
    if db_updater: db_updater(current_state)

    # Step 2: Plan Campaign
    out_plan = node_plan_campaign(current_state)
    current_state.update(out_plan)
    if db_updater: db_updater(current_state)

    # Step 3 & 4: Content Generation + Quality Check Loop (Before Media Generation)
    max_retries = current_state.get("max_qc_retries", 3)
    for attempt in range(max_retries):
        out_content = node_generate_content(current_state)
        current_state.update(out_content)
        if db_updater: db_updater(current_state)

        out_qc = node_quality_check(current_state)
        current_state.update(out_qc)
        if db_updater: db_updater(current_state)

        if current_state.get("qc_passed", False):
            break

    # Step 5: Parallel Media Generation (Poster & Video generated in parallel threads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_poster = executor.submit(node_generate_poster, dict(current_state))
        future_video = executor.submit(node_generate_video, dict(current_state))

        poster_res = future_poster.result()
        video_res = future_video.result()

    current_state.update(poster_res)
    current_state.update(video_res)

    # Step 6: Combine Media
    out_combine = node_combine_media(current_state)
    current_state.update(out_combine)
    if db_updater: db_updater(current_state)

    # Step 7: Human Approval Checkpoint
    out_approval = node_human_approval(current_state)
    current_state.update(out_approval)
    if db_updater: db_updater(current_state)

    return current_state

def resume_and_publish_workflow(current_state: MarketingWorkflowState, db_updater=None) -> Dict[str, Any]:
    """Resumes approved campaign to trigger parallel publishing to YouTube, Instagram, and Facebook."""
    current_state["approval_status"] = "APPROVED"
    out_approval = node_human_approval(current_state)
    current_state.update(out_approval)
    if db_updater: db_updater(current_state)

    out_pub = node_publish_parallel(current_state)
    current_state.update(out_pub)
    if db_updater: db_updater(current_state)

    return current_state
