import os
import sys
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render page numbers (Page X of Y)
    along with running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress headers/footers on the first (Cover) page
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569")) # Slate 600
            self.drawString(54, 752, "HERWATCH: WOMEN SAFETY ANALYTICS SYSTEM")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#94A3B8")) # Slate 400
            self.drawRightString(558, 752, "END-TO-END TECHNICAL SPECIFICATION")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0")) # Slate 200
            self.setLineWidth(0.75)
            self.line(54, 744, 558, 744)

            # Footer
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 48, 558, 48)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 34, "Confidential & Proprietary — HerWatch Safety System")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 34, page_text)
            
        self.restoreState()


def create_herwatch_report(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,  # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#881337")    # Rose 900 / Crimson
    SECONDARY = colors.HexColor("#BE123C")  # Rose 700
    ACCENT = colors.HexColor("#0284C7")     # Sky 600
    DARK_BG = colors.HexColor("#0F172A")    # Slate 900
    TEXT_COLOR = colors.HexColor("#1E293B") # Slate 800
    MUTED_TEXT = colors.HexColor("#475569") # Slate 600
    CARD_BG = colors.HexColor("#F8FAFC")    # Slate 50
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=PRIMARY,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=20,
        textColor=MUTED_TEXT,
        spaceAfter=25
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=MUTED_TEXT
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=SECONDARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=DARK_BG,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_COLOR,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0369A1")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_COLOR
    )

    story = []

    # ==========================================
    # COVER PAGE / HEADER BLOCK
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("🚨 HERWATCH: WOMEN SAFETY ANALYTICS SYSTEM", title_style))
    story.append(Paragraph("A Real-Time Computer Vision & Geospatial Surveillance Framework for Enhanced Public Safety", subtitle_style))
    
    story.append(HRFlowable(width="100%", thickness=3, color=PRIMARY, spaceBefore=0, spaceAfter=20))

    # Executive Overview Box
    overview_text = (
        "<b>Executive Summary:</b> HerWatch is an end-to-end intelligent safety surveillance system "
        "combining state-of-the-art computer vision (YOLOv8, MediaPipe, MobileNetV2) and geospatial analytics "
        "(Folium, Geopy) to protect women in urban and semi-urban environments. The system delivers real-time "
        "distress signal detection, automated nocturnal lone-woman identification, contextual crowd gender monitoring, "
        "and interactive crime hotspot visualization over a responsive React dashboard."
    )
    
    overview_table = Table(
        [[Paragraph(overview_text, callout_style)]],
        colWidths=[504]
    )
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E0F2FE")), # Sky 100
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#38BDF8")),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 20))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Project Version:</b> 1.0.0 Production", meta_style), Paragraph("<b>Tech Stack:</b> Python (Flask), React.js, PyTorch, OpenCV", meta_style)],
        [Paragraph("<b>Target Domain:</b> Public Safety & Smart Cities", meta_style), Paragraph("<b>AI Architecture:</b> YOLOv8 + MediaPipe + MobileNetV2", meta_style)],
        [Paragraph("<b>Document Type:</b> End-to-End System Report", meta_style), Paragraph(f"<b>Generated Date:</b> August 2026", meta_style)],
    ]
    meta_table = Table(meta_data, colWidths=[252, 252])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 25))

    # ==========================================
    # SECTION 1: PROBLEM STATEMENT & VISION
    # ==========================================
    story.append(Paragraph("1. Problem Statement & Strategic Vision", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=10))
    
    p1 = (
        "Women's safety in public spaces remains a critical global challenge, particularly during late hours or in "
        "isolated transit areas. Traditional CCTV networks are inherently passive—requiring continuous human monitoring "
        "which is prone to fatigue, latency, and delayed emergency response. Furthermore, conventional security systems "
        "lack situational awareness regarding distress gestures, gender dynamics, and localized crime historical data."
    )
    story.append(Paragraph(p1, body_style))

    p2 = (
        "<b>HerWatch</b> addresses these shortcomings by introducing an proactive, AI-driven surveillance framework that "
        "automatically monitors live video streams and recorded feeds to identify high-risk scenarios in real-time. By "
        "combining spatial crime intelligence with multi-modal deep learning models, HerWatch empowers municipal authorities, "
        "campus security, and law enforcement with actionable alerts."
    )
    story.append(Paragraph(p2, body_style))

    # Core Vision Pillars
    story.append(Paragraph("Key Strategic Pillars:", h3_style))
    story.append(Paragraph("• <b>Proactive Distress Detection:</b> Instant recognition of non-verbal SOS gestures (hand waving, double hand raise, cover mouth) without physical button pressing.", bullet_style))
    story.append(Paragraph("• <b>Nocturnal Contextual Risk Assessment:</b> Detecting solitary women during high-risk nighttime hours (19:00 - 06:00) with rapid male/female crowd ratio analysis.", bullet_style))
    story.append(Paragraph("• <b>Geospatial Crime Intelligence:</b> Dynamic crime hotspot mapping and proximity calculations against historical district-level Indian crime datasets.", bullet_style))
    story.append(Paragraph("• <b>Dual-Mode Accessibility:</b> Supporting both low-latency live camera streaming (WebSocket) and file-based recorded video processing.", bullet_style))

    story.append(Spacer(1, 15))

    # ==========================================
    # SECTION 2: SYSTEM ARCHITECTURE & DATAFLOW
    # ==========================================
    story.append(Paragraph("2. System Architecture & High-Level Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph(
        "HerWatch employs a decoupled client-server architecture. The backend is powered by Flask and OpenCV, executing heavy AI pipeline processing. "
        "The frontend is built with React.js, providing real-time dashboard analytics, WebSocket video feeds, and interactive map displays.",
        body_style
    ))

    # System Architecture Component Table
    arch_headers = [Paragraph("Component Layer", table_header_style), Paragraph("Technologies Used", table_header_style), Paragraph("Key Responsibilities", table_header_style)]
    arch_rows = [
        [
            Paragraph("<b>Frontend UI Layer</b>", table_body_style),
            Paragraph("React 18, Material-UI, Framer Motion, Chart.js", table_body_style),
            Paragraph("Live alert monitoring, interactive hotspot maps, video upload UI, gesture status telemetry.", table_body_style)
        ],
        [
            Paragraph("<b>API & WebSocket Backend</b>", table_body_style),
            Paragraph("Flask 3.1, Flask-CORS, Flask-Sock (WebSocket)", table_body_style),
            Paragraph("RESTful endpoints (`/api/hotspots/analyze`), WebSocket camera feed handlers (`/ws/camera`), static serving.", table_body_style)
        ],
        [
            Paragraph("<b>Object Detection Engine</b>", table_body_style),
            Paragraph("YOLOv8 (Ultralytics), PyTorch, OpenCV", table_body_style),
            Paragraph("Real-time person bounding box detection (`class=0`), confidence thresholding (>0.4), tracking.", table_body_style)
        ],
        [
            Paragraph("<b>Gesture Detection Pipeline</b>", table_body_style),
            Paragraph("MediaPipe Holistic Solution (3D Keypoints)", table_body_style),
            Paragraph("Hand & body pose landmark tracking; wave frequency analysis, hand-above-wrist elevation logic.", table_body_style)
        ],
        [
            Paragraph("<b>Gender Classification Engine</b>", table_body_style),
            Paragraph("MobileNetV2 (PyTorch Torchvision Weights)", table_body_style),
            Paragraph("Face region cropping from person bboxes, image normalization, gender probability inference.", table_body_style)
        ],
        [
            Paragraph("<b>Geospatial Engine</b>", table_body_style),
            Paragraph("Folium, Leaflet.js, Geopy (Nominatim & Geodesic)", table_body_style),
            Paragraph("District geocoding, geodesic distance calculation (<100km radius), interactive risk circle rendering.", table_body_style)
        ]
    ]

    arch_table = Table([arch_headers] + arch_rows, colWidths=[120, 140, 244])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 15))

    story.append(PageBreak()) # Clean transition to detailed module sections

    # ==========================================
    # SECTION 3: CORE AI MODULES DEEP DIVE
    # ==========================================
    story.append(Paragraph("3. Core AI Modules & Deep Learning Pipeline", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    # Sub-section 3.1: SOS Gesture Detection
    story.append(Paragraph("3.1 SOS Distress Gesture Detection Engine", h2_style))
    p_sos = (
        "The distress gesture module utilizes <b>MediaPipe Holistic</b> to extract 33 pose landmarks and 21 hand keypoints per hand in real-time. "
        "It runs heuristic geometric evaluation on body coordinates without requiring heavy custom gesture training models, ensuring sub-50ms latency."
    )
    story.append(Paragraph(p_sos, body_style))

    story.append(Paragraph("Detection Logic & Mathematical Conditions:", h3_style))
    story.append(Paragraph("• <b>Raised Hand Gesture:</b> Evaluates if <code>Middle_Finger_Tip.y < Wrist.y</code> and <code>Wrist.y < 0.5</code> (upper frame half).", bullet_style))
    story.append(Paragraph("• <b>Hand Waving Gesture:</b> Tracks horizontal displacement <code>|Middle_Tip.x - Wrist.x| > 0.15</code> combined with vertical displacement <code>> 0.25</code> over a sliding 2.0-second time window.", bullet_style))
    story.append(Paragraph("• <b>Double Hand SOS:</b> Validates both left and right hand keypoints simultaneously elevated above shoulder line (<code>Left_Wrist.y < Left_Shoulder.y</code> & <code>Right_Wrist.y < Right_Shoulder.y</code>).", bullet_style))
    story.append(Paragraph("• <b>Hand Over Mouth Sign:</b> Calculates Euclidean distance between <code>Hand_Landmarks</code> and <code>Mouth_Landmark</code> (threshold <code>< 0.15</code> normalized units).", bullet_style))

    story.append(Spacer(1, 10))

    # Sub-section 3.2: Lone Woman at Night & Gender Classification
    story.append(Paragraph("3.2 Lone Woman Detection at Night & Gender Analytics", h2_style))
    p_lone = (
        "Solitary exposure during late hours represents one of the highest statistical risk scenarios for women in urban transit zones. "
        "HerWatch combines temporal monitoring with person detection and deep-learning gender classification."
    )
    story.append(Paragraph(p_lone, body_style))

    story.append(Paragraph("Processing Pipeline Breakdown:", h3_style))
    story.append(Paragraph("1. <b>Nocturnal Time Filter:</b> Checks system timestamp; triggers active lone-woman assessment if local time falls between <code>19:00</code> (7 PM) and <code>06:00</code> (6 AM).", bullet_style))
    story.append(Paragraph("2. <b>Person Detection (YOLOv8n):</b> Scans image frame for objects with COCO class ID <code>0 (person)</code>. Detections below <code>0.40</code> confidence are filtered out.", bullet_style))
    story.append(Paragraph("3. <b>Face / Body Extraction:</b> Crops upper 60% of bounding box (representing head and torso) for gender classification.", bullet_style))
    story.append(Paragraph("4. <b>MobileNetV2 Inference:</b> Resizes crop to <code>224x224 RGB</code>, normalizes tensor values, and feeds into MobileNetV2. Softmax activation predicts <code>Female vs Male</code> confidence score.", bullet_style))
    story.append(Paragraph("5. <b>Lone Woman Rule Evaluation:</b> If <code>Total_Persons == 1</code>, <code>Gender == Female</code>, <code>Confidence >= 0.60</code>, and <code>is_nighttime() == True</code>, an emergency <b>LONE WOMAN AT NIGHT</b> alert is dispatched.", bullet_style))

    story.append(Spacer(1, 10))

    # Sub-section 3.3: Geospatial Crime Hotspot Engine
    story.append(Paragraph("3.3 Geospatial Crime Hotspot Mapping & Geocoding", h2_style))
    p_geo = (
        "HerWatch incorporates district-level historical crime dataset (<code>women-crimedataset-India.csv</code>) covering multiple crime categories "
        "including Rape, Kidnapping & Abduction, Dowry Deaths, Assault on Women, and Cruelty by Husband/Relatives."
    )
    story.append(Paragraph(p_geo, body_style))

    story.append(Paragraph("Geospatial Distance & Risk Assessment Algorithm:", h3_style))
    story.append(Paragraph("• <b>Geocoding with Nominatim:</b> User inputs city/district name (e.g., 'Bengaluru'). Nominatim API returns exact <code>(latitude, longitude)</code> coordinates with automatic retry logic.", bullet_style))
    story.append(Paragraph("• <b>Geodesic Distance Computation:</b> Computes great-circle distance between user location \\(P_{user}\\) and every district \\(P_{district}\\) using Geopy's geodesic formula:", bullet_style))
    
    geo_formula_text = "<b>Distance Formula:</b> d = 2R · arcsin( √( sin²(Δlat/2) + cos(lat1)·cos(lat2)·sin²(Δlon/2) ) )"
    story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<i>{geo_formula_text}</i>", body_style))
    
    story.append(Paragraph("• <b>Proximity Filter:</b> Filters all crime records within a <b>100 km radius</b>.", bullet_style))
    story.append(Paragraph("• <b>Risk Categorization:</b> Assigns risk levels based on total crimes reported: High Risk (Red Circle, >1000 incidents), Medium Risk (Orange Circle), Low Risk (Green Circle).", bullet_style))

    story.append(Spacer(1, 15))

    # ==========================================
    # SECTION 4: BACKEND & API SPECIFICATIONS
    # ==========================================
    story.append(Paragraph("4. Backend Architecture & REST/WebSocket API Reference", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph(
        "The Flask backend server (`app.py`) runs on port <code>5001</code> and serves both RESTful endpoints and high-performance WebSockets for live video streaming.",
        body_style
    ))

    # API Endpoints Table
    api_headers = [Paragraph("HTTP/WS Method", table_header_style), Paragraph("Endpoint Route", table_header_style), Paragraph("Description & Output Schema", table_header_style)]
    api_rows = [
        [
            Paragraph("<code>GET</code>", table_body_style),
            Paragraph("<code>/api/health</code>", table_body_style),
            Paragraph("Health check endpoint. Returns <code>{\"status\": \"ok\", \"message\": \"API is running\"}</code>.", table_body_style)
        ],
        [
            Paragraph("<code>POST</code>", table_body_style),
            Paragraph("<code>/api/hotspots/analyze</code>", table_body_style),
            Paragraph("Accepts location name or lat/lon coordinates. Computes nearby crime hotspots within 100km and returns Folium interactive map HTML string.", table_body_style)
        ],
        [
            Paragraph("<code>POST</code>", table_body_style),
            Paragraph("<code>/analyze_video</code>", table_body_style),
            Paragraph("Uploads video file (`multipart/form-data`). Runs frame-by-frame YOLOv8 + MediaPipe analysis and generates processed output video file.", table_body_style)
        ],
        [
            Paragraph("<code>GET</code>", table_body_style),
            Paragraph("<code>/api/live-camera/list</code>", table_body_style),
            Paragraph("Enumerates connected physical webcams/cameras using OpenCV device index probing (`cv2.VideoCapture(i)`).", table_body_style)
        ],
        [
            Paragraph("<code>WebSocket</code>", table_body_style),
            Paragraph("<code>/ws/camera</code>", table_body_style),
            Paragraph("Bidirectional socket. Receives Base64 encoded JPEG video frames from frontend; sends processed frame Base64 with alert telemetry JSON payload.", table_body_style)
        ],
    ]

    api_table = Table([api_headers] + api_rows, colWidths=[90, 150, 264])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(api_table)
    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # ==========================================
    # SECTION 5: FRONTEND APPLICATION (REACT.JS)
    # ==========================================
    story.append(Paragraph("5. Frontend Application Architecture (React.js)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph(
        "The React frontend (`sos-detection-frontend`) provides a modern, responsive UI crafted with Material-UI (MUI v5) and Framer Motion animations. "
        "It features dynamic tab routing for seamless navigation across all core functions.",
        body_style
    ))

    # Page Component Breakdown
    story.append(Paragraph("Frontend Page Breakdown:", h3_style))
    
    fe_headers = [Paragraph("Page Component", table_header_style), Paragraph("File Path", table_header_style), Paragraph("Key Features & User Interactions", table_header_style)]
    fe_rows = [
        [
            Paragraph("<b>Live Camera Stream</b>", table_body_style),
            Paragraph("<code>src/pages/LiveCamera.js</code>", table_body_style),
            Paragraph("Selects active webcam, opens WebSocket stream to Flask, renders annotated live video canvas, triggers auditory alert sounds, displays active threat banner.", table_body_style)
        ],
        [
            Paragraph("<b>Video Analysis Mode</b>", table_body_style),
            Paragraph("<code>src/pages/VideoMode.js</code>", table_body_style),
            Paragraph("Drag-and-drop video uploader (`.mp4`, `.avi`), progress indicator bar, frame playback, detected threats timeline log.", table_body_style)
        ],
        [
            Paragraph("<b>Hotspot Risk Map</b>", table_body_style),
            Paragraph("<code>src/pages/HotspotMap.js</code>", table_body_style),
            Paragraph("Location search input, 'Use My Current GPS Location' button, embedded Folium Leaflet interactive heatmap, crime statistic breakdown cards.", table_body_style)
        ],
        [
            Paragraph("<b>Analytics Dashboard</b>", table_body_style),
            Paragraph("<code>src/pages/Dashboard.js</code>", table_body_style),
            Paragraph("Chart.js visual charts displaying total incident breakdown (Rape, Assault, Kidnapping) and hourly risk distribution.", table_body_style)
        ],
    ]

    fe_table = Table([fe_headers] + fe_rows, colWidths=[120, 150, 234])
    fe_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(fe_table)
    story.append(Spacer(1, 15))

    # ==========================================
    # SECTION 6: INSTALLATION & OPERATIONAL GUIDE
    # ==========================================
    story.append(Paragraph("6. Installation, Configuration & Deployment Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph("Prerequisites:", h3_style))
    story.append(Paragraph("• Python 3.10+ (Virtual environment recommended)", bullet_style))
    story.append(Paragraph("• Node.js 18+ and npm 9+", bullet_style))
    story.append(Paragraph("• Webcam device (for live streaming mode)", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Step 1: Backend Setup & Execution", h2_style))
    
    b_code = (
        "cd \"/Users/spurthinaveli/Desktop/Herwatch/ThemeBased Code\"<br/>"
        "source venv/bin/activate<br/>"
        "# Install dependencies if setting up fresh:<br/>"
        "pip install -r requirements.txt<br/>"
        "pip install \"numpy<2\" reportlab<br/>"
        "python app.py"
    )
    b_table = Table([[Paragraph(f"<code>{b_code}</code>", table_body_style)]], colWidths=[504])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(b_table)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Step 2: Frontend Setup & Execution", h2_style))
    
    f_code = (
        "cd \"/Users/spurthinaveli/Desktop/Herwatch/ThemeBased Code/sos-detection-frontend\"<br/>"
        "# Start React Development Server:<br/>"
        "npm start"
    )
    f_table = Table([[Paragraph(f"<code>{f_code}</code>", table_body_style)]], colWidths=[504])
    f_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(f_table)

    story.append(Spacer(1, 15))

    # ==========================================
    # SECTION 7: FUTURE SCOPE & CONCLUSION
    # ==========================================
    story.append(Paragraph("7. Future Scope & System Enhancements", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph("• <b>Audio Distress Recognition:</b> Integrating micro-acoustic neural networks (such as YAMNet or PyAudio) to detect screams, glass breaking, and vocal distress cues in ambient audio feeds.", bullet_style))
    story.append(Paragraph("• <b>Edge Computing Deployment:</b> Quantizing YOLOv8 and MobileNetV2 models for TensorRT / ONNX runtime to deploy on edge AI hardware (Nvidia Jetson Orin Nano, Raspberry Pi 5).", bullet_style))
    story.append(Paragraph("• <b>Automated Emergency Dispatch:</b> Integrating Twilio API to automatically dispatch real-time SMS alerts with live GPS pin coordinates to designated emergency contacts and local police authorities.", bullet_style))
    story.append(Paragraph("• <b>Infrared / Thermal Camera Support:</b> Fine-tuning person and pose detection pipelines on thermal and night-vision video channels for zero-light environment detection.", bullet_style))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=MUTED_TEXT, spaceBefore=10, spaceAfter=15))
    story.append(Paragraph("<i>End of HerWatch Technical Report — Generated automatically for HerWatch Women Safety Project.</i>", meta_style))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_filename}")

if __name__ == '__main__':
    output_pdf_path = "/Users/spurthinaveli/Desktop/Herwatch/HerWatch_End_to_End_Project_Report.pdf"
    create_herwatch_report(output_pdf_path)
