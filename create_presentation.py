#!/usr/bin/env python3
"""
Create PowerPoint presentation for Tanzanian Water Wells project
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pathlib import Path
import os

# Define color scheme
PRIMARY_COLOR = RGBColor(41, 128, 185)  # Blue
ACCENT_COLOR = RGBColor(46, 204, 113)  # Green
DANGER_COLOR = RGBColor(231, 76, 60)   # Red
WARNING_COLOR = RGBColor(243, 156, 18)  # Orange
TEXT_COLOR = RGBColor(44, 62, 80)      # Dark gray

def add_title_slide(prs, title, subtitle):
    """Add a title slide"""
    slide_layout = prs.slide_layouts[0]  # Title slide layout
    slide = prs.slides.add_slide(slide_layout)
    
    title_shape = slide.shapes.title
    subtitle_shape = slide.placeholders[1]
    
    title_shape.text = title
    subtitle_shape.text = subtitle
    
    # Format title
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(44)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Format subtitle
    subtitle_frame = subtitle_shape.text_frame
    subtitle_frame.paragraphs[0].font.size = Pt(20)
    subtitle_frame.paragraphs[0].font.color.rgb = TEXT_COLOR
    
    return slide

def add_content_slide(prs, title, content_dict=None, image_path=None):
    """Add a content slide with optional bullet points and image"""
    slide_layout = prs.slide_layouts[5]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Add content if provided
    if content_dict:
        content_top = Inches(1.3)
        content_box = slide.shapes.add_textbox(Inches(0.5), content_top, 
                                                Inches(4.5) if image_path else Inches(9), 
                                                Inches(5))
        text_frame = content_box.text_frame
        text_frame.word_wrap = True
        
        for key, value in content_dict.items():
            p = text_frame.add_paragraph()
            p.text = f"{key}: {value}"
            p.font.size = Pt(14)
            p.font.color.rgb = TEXT_COLOR
            p.space_after = Pt(8)
            p.level = 0
    
    # Add image if provided
    if image_path and os.path.exists(image_path):
        left = Inches(5.2) if content_dict else Inches(0.5)
        top = Inches(1.3)
        width = Inches(4.5) if content_dict else Inches(9)
        slide.shapes.add_picture(image_path, left, top, width=width)
    
    return slide

def add_full_image_slide(prs, title, image_path):
    """Add a slide with title and full-width image"""
    slide_layout = prs.slide_layouts[5]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Add image
    if os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(0.5), Inches(1.2), width=Inches(9))
    
    return slide

def add_bullet_slide(prs, title, bullets):
    """Add a slide with bullet points"""
    slide_layout = prs.slide_layouts[5]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Add bullets
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(8.4), Inches(5))
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    for i, bullet in enumerate(bullets):
        p = text_frame.add_paragraph() if i > 0 else text_frame.paragraphs[0]
        p.text = bullet
        p.font.size = Pt(16)
        p.font.color.rgb = TEXT_COLOR
        p.space_after = Pt(12)
        p.level = 0
    
    return slide

# Create presentation
print("Creating PowerPoint presentation...")
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Slide 1: Title Slide
print("Adding title slide...")
add_title_slide(prs, 
                "Tanzanian Water Wells\nPredictive Maintenance Analysis",
                "Data-Driven Insights for Water Infrastructure Management\nJanuary 2026")

# Slide 2: Project Overview
print("Adding project overview...")
overview_content = {
    "📊 Objective": "Predict water well functionality to optimize maintenance",
    "🌍 Scope": "59,400 water wells across Tanzania",
    "🎯 Target": "3-class classification (functional, needs repair, non-functional)",
    "📈 Approach": "Exploratory data analysis and predictive insights",
    "💡 Goal": "Enable proactive maintenance and resource allocation"
}
add_content_slide(prs, "Project Overview", overview_content)

# Slide 3: Data Landscape
print("Adding data landscape slide...")
data_content = {
    "Training Data": "59,400 wells with 40 features",
    "Test Data": "14,850 wells for evaluation",
    "Feature Types": "9 numeric, 31 categorical",
    "Geographic Coverage": "Multiple regions across Tanzania",
    "Temporal Range": "Construction years 1960-2013",
    "Data Quality": "Some missing values in funder, installer, scheme_name"
}
add_content_slide(prs, "Data Landscape", data_content)

# Slide 4: Target Distribution
print("Adding target distribution slide...")
add_full_image_slide(prs, "Target Distribution: Well Status Breakdown",
                     "visualizations/01_target_distribution.png")

# Slide 5: Key Finding - Water Quantity
print("Adding water quantity analysis...")
add_full_image_slide(prs, "Key Finding: Water Quantity as Primary Predictor",
                     "visualizations/02_water_quantity_analysis.png")

# Slide 6: Geographic Distribution
print("Adding geographic distribution...")
add_full_image_slide(prs, "Geographic Distribution of Water Wells",
                     "visualizations/03_geographic_distribution.png")

# Slide 7: Temporal Analysis
print("Adding construction year analysis...")
add_full_image_slide(prs, "Temporal Analysis: Well Status by Construction Era",
                     "visualizations/04_construction_year_analysis.png")

# Slide 8: Regional Insights
print("Adding regional analysis...")
add_full_image_slide(prs, "Regional Distribution and Status Patterns",
                     "visualizations/05_regional_analysis.png")

# Slide 9: Waterpoint Types
print("Adding waterpoint type analysis...")
add_full_image_slide(prs, "Infrastructure Analysis: Waterpoint Types",
                     "visualizations/06_waterpoint_type_analysis.png")

# Slide 10: Data Quality
print("Adding data quality slide...")
add_full_image_slide(prs, "Data Quality Assessment: Missing Values",
                     "visualizations/07_missing_data_overview.png")

# Slide 11: Population Analysis
print("Adding population analysis...")
add_full_image_slide(prs, "Population Served Analysis",
                     "visualizations/08_population_analysis.png")

# Slide 12: Insights Dashboard
print("Adding insights dashboard...")
add_full_image_slide(prs, "Executive Dashboard: Key Insights",
                     "visualizations/09_insights_dashboard.png")

# Slide 13: Key Insights Summary
print("Adding key insights summary...")
insights_bullets = [
    "🔑 Water Quantity is the strongest predictor: 96.9% of 'dry' wells are non-functional",
    "📍 Geographic clustering: Certain regions show higher failure rates",
    "⏰ Age matters: Older wells (pre-1990) have higher failure rates",
    "🏗️ Infrastructure type impacts reliability: Communal standpipes most common",
    "👥 Population dependency: 54.3% of wells are functional, serving millions",
    "📊 Data gaps: 48.5% missing scheme_name, 56.0% missing permit data",
    "🎯 Actionable: Focus maintenance on dry/insufficient water quantity wells"
]
add_bullet_slide(prs, "Key Insights Summary", insights_bullets)

# Slide 14: Business Impact
print("Adding business impact slide...")
impact_bullets = [
    "💰 Cost Optimization: Target maintenance resources to high-risk wells",
    "⚡ Proactive Intervention: Predict failures before they occur",
    "📈 Service Reliability: Improve functional well percentage from 54.3%",
    "🎯 Resource Allocation: Prioritize regions with highest failure rates",
    "📊 Data-Driven Decisions: Evidence-based infrastructure planning",
    "🌊 Water Security: Ensure continuous access to clean water for communities",
    "🔄 Maintenance Scheduling: Optimize repair cycles based on predictive signals"
]
add_bullet_slide(prs, "Business Impact & Value Proposition", impact_bullets)

# Slide 15: Recommendations
print("Adding recommendations slide...")
recommendations = [
    "1. Immediate Action: Inspect all wells with 'dry' or 'insufficient' water quantity",
    "2. Geographic Focus: Deploy teams to high-failure regions (Iringa, Mbeya, Arusha)",
    "3. Age-Based Maintenance: Prioritize wells constructed before 1990",
    "4. Data Collection: Improve tracking of scheme_name, permits, and maintenance logs",
    "5. Monitoring Systems: Implement real-time water quantity sensors",
    "6. Community Engagement: Train local managers on early warning signs",
    "7. Predictive Models: Deploy classification models for ongoing risk assessment"
]
add_bullet_slide(prs, "Strategic Recommendations", recommendations)

# Slide 16: Data Collection Improvements
print("Adding data collection improvements...")
improvements = [
    "📝 Standardize Data Entry: Consistent formats for funder, installer, scheme_name",
    "🔍 Reduce Missing Values: Target <10% missingness for critical features",
    "📱 Digital Tools: Mobile apps for field data collection and validation",
    "🗓️ Regular Updates: Monthly status checks for all wells",
    "📊 Quality Metrics: Track data completeness and accuracy over time",
    "🔗 Integration: Link well data with maintenance records and community feedback",
    "🎓 Training: Field staff education on data quality importance"
]
add_bullet_slide(prs, "Data Collection & Quality Improvements", improvements)

# Slide 17: Next Steps
print("Adding next steps slide...")
next_steps = [
    "✅ Phase 1: Validate insights with domain experts and field teams",
    "✅ Phase 2: Deploy pilot maintenance program in top 3 high-risk regions",
    "✅ Phase 3: Implement monitoring dashboard for real-time status tracking",
    "✅ Phase 4: Build and deploy predictive model for failure forecasting",
    "✅ Phase 5: Scale successful interventions nationwide",
    "✅ Phase 6: Establish feedback loop for continuous improvement",
    "📅 Timeline: 6-12 months for full implementation"
]
add_bullet_slide(prs, "Next Steps & Roadmap", next_steps)

# Slide 18: Closing Slide
print("Adding closing slide...")
closing_content = {
    "Impact": "Improving water access for millions of Tanzanians",
    "Approach": "Data-driven predictive maintenance",
    "Status": "Analysis complete, ready for implementation",
    "Contact": "Ready for stakeholder review and deployment planning"
}
add_content_slide(prs, "Thank You", closing_content)

# Save presentation
output_file = "Tanzania_Water_Wells_Presentation.pptx"
prs.save(output_file)
print(f"\n✓ Presentation saved as '{output_file}'")
print(f"  Total slides: {len(prs.slides)}")
print(f"  Format: PowerPoint (.pptx)")
print(f"  Dimensions: 10\" x 7.5\"")
