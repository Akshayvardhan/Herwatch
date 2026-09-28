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
        
        # Suppress headers/footers on cover page
        if self._pageNumber > 1:
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E293B")) # Slate 800
            self.drawString(54, 752, "HERWATCH — COMPLETE PROJECT INTERVIEW PREPARATION GUIDE")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B")) # Slate 500
            self.drawRightString(558, 752, "FULL CODEBASE & TECHNICAL DEEP DIVE")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1")) # Slate 300
            self.setLineWidth(0.75)
            self.line(54, 744, 558, 744)

            # Running Footer
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 48, 558, 48)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 34, "Personal Interview Study Guide — HerWatch Women Safety Analytics System")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 34, page_text)
            
        self.restoreState()


def build_interview_preparation_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,  # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Professional Color Palette
    PRIMARY = colors.HexColor("#0F172A")     # Deep Navy / Slate 900
    SECONDARY = colors.HexColor("#881337")   # Rose 900 / Dark Crimson
    ACCENT_BLUE = colors.HexColor("#0284C7") # Sky 600
    TEXT_DARK = colors.HexColor("#1E293B")   # Slate 800
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600
    BG_CARD = colors.HexColor("#F8FAFC")     # Slate 50
    BORDER_LIGHT = colors.HexColor("#E2E8F0")# Slate 200
    CODE_BG = colors.HexColor("#F1F5F9")     # Slate 100

    # Custom Typography Styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=PRIMARY,
        spaceAfter=10
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=SECONDARY,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'H3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=4,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#0369A1")
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    tbl_body_style = ParagraphStyle(
        'TblBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )

    story = []

    # =========================================================================
    # COVER / HEADER BLOCK
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("🎓 HerWatch: Complete Technical Interview Preparation Guide", cover_title_style))
    story.append(Paragraph("Comprehensive Codebase Analysis, System Architecture, Code Tracing, 50+ Q&amp;A, and Cheat Sheet", cover_subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2.5, color=PRIMARY, spaceBefore=0, spaceAfter=15))

    # Meta Overview Box
    meta_box_text = (
        "<b>Document Purpose:</b> This study guide is built strictly from the ground-up analysis of the <b>HerWatch</b> "
        "repository. It breaks down every single component—from the Flask backend and WebSocket camera streams to the "
        "YOLOv8, MediaPipe, and MobileNetV2 deep learning engines, and React.js dashboard. It equips you with 30-second pitches, "
        "step-by-step code traces, file rankings, 50+ interview Q&amp;As, 17 difficult follow-ups, and line-by-line code explanations."
    )
    meta_table = Table([[Paragraph(meta_box_text, callout_style)]], colWidths=[504])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#38BDF8")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 1: PROJECT ANALYSIS & STRUCTURE
    # =========================================================================
    story.append(Paragraph("1. Complete Project Structure & File Map", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "The project is structured into two main directories: the Python Flask backend root (`ThemeBased Code/`) and "
        "the React frontend single-page application (`ThemeBased Code/sos-detection-frontend/`). Below is the exact file layout:",
        body_style
    ))

    struct_code = (
        "Herwatch/<br/>"
        "├── README.md                           # Main project documentation &amp; feature overview<br/>"
        "├── women-crimedataset-India.csv        # Historical district crime statistics in India<br/>"
        "└── ThemeBased Code/<br/>"
        "    ├── app.py                          # Main Flask server entry point &amp; REST/WebSocket endpoints<br/>"
        "    ├── live_camera_processor.py        # Real-time webcam frame processor (YOLOv8 + MediaPipe + MobileNet)<br/>"
        "    ├── video_processor.py              # Recorded video file batch processor<br/>"
        "    ├── crime_hotspot_map.html          # Folium-generated HTML Leaflet map overlay<br/>"
        "    ├── requirements.txt                # Python package dependency list<br/>"
        "    ├── yolov8n.pt                      # Pretrained YOLOv8 Nano weights for person detection<br/>"
        "    ├── venv/                           # Python 3.10 virtual environment directory<br/>"
        "    └── sos-detection-frontend/         # React 18 Frontend Application Root<br/>"
        "        ├── package.json                # Node dependencies &amp; npm start/build scripts<br/>"
        "        └── src/<br/>"
        "            ├── App.js                  # Main React component, ThemeProvider &amp; React-Router routes<br/>"
        "            ├── index.js                # React DOM render entry point<br/>"
        "            ├── components/<br/>"
        "            │   ├── Navbar.js           # Navigation top bar with links &amp; branding<br/>"
        "            │   └── Layout.js           # Master layout wrapper containing Navbar and Outlet<br/>"
        "            └── pages/<br/>"
        "                ├── Home.js             # Landing hero page with system capabilities<br/>"
        "                ├── LiveCamera.js       # Real-time WebSocket webcam streaming &amp; alert UI<br/>"
        "                ├── VideoMode.js        # File drag-and-drop video processing UI<br/>"
        "                ├── HotspotMap.js       # Interactive crime hotspot search &amp; map page<br/>"
        "                ├── Dashboard.js        # Analytics page featuring Chart.js crime statistics<br/>"
        "                ├── Login.js            # User authentication sign-in form (Mock UI)<br/>"
        "                ├── Register.js         # User registration form (Mock UI)<br/>"
        "                ├── Profile.js          # User profile management page (Mock UI)<br/>"
        "                └── About.js            # Project mission and team information page"
    )
    
    struct_table = Table([[Paragraph(f"<code>{struct_code}</code>", code_style)]], colWidths=[504])
    struct_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(struct_table)
    story.append(Spacer(1, 12))

    # File descriptions
    story.append(Paragraph("Key File Responsibilities:", h3_style))
    story.append(Paragraph("• <b>app.py:</b> Initializes Flask app, configures CORS, loads CSV dataset into Pandas DataFrame, hosts REST routes (`/api/health`, `/api/hotspots/analyze`, `/analyze_video`) and WebSocket handler (`/ws/camera`).", bullet_style))
    story.append(Paragraph("• <b>live_camera_processor.py:</b> Contains `process_live_camera(frame)`. Performs frame decoding, YOLOv8 person detection, MediaPipe Holistic gesture checks, MobileNetV2 gender classification, and draws red alert visual overlays.", bullet_style))
    story.append(Paragraph("• <b>video_processor.py:</b> Implements frame-by-frame batch processing (`process_video_combined`) for uploaded MP4/AVI files, exporting annotated output videos.", bullet_style))
    story.append(Paragraph("• <b>LiveCamera.js:</b> Captures browser canvas/webcam images at intervals, sends Base64 JPEG frames via WebSocket (`ws://localhost:5001/ws/camera`), and displays real-time alert badges.", bullet_style))
    story.append(Paragraph("• <b>HotspotMap.js:</b> Queries Geopy/Folium endpoint, displays district crime counts within 100km, and embeds interactive Leaflet HTML maps inside an iframe.", bullet_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 2: TECHNOLOGY STACK MATRIX
    # =========================================================================
    story.append(Paragraph("2. Complete Technology Stack Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    tech_headers = [Paragraph("Layer", tbl_header_style), Paragraph("Technology", tbl_header_style), Paragraph("Why It Is Used", tbl_header_style), Paragraph("Where It Appears in Code", tbl_header_style)]
    tech_rows = [
        [
            Paragraph("Frontend Framework", tbl_body_style),
            Paragraph("React 18.2", tbl_body_style),
            Paragraph("Builds responsive, component-driven user interface with dynamic state re-rendering.", tbl_body_style),
            Paragraph("<code>sos-detection-frontend/src/</code>", tbl_body_style)
        ],
        [
            Paragraph("UI Component Library", tbl_body_style),
            Paragraph("Material-UI (MUI v5)", tbl_body_style),
            Paragraph("Provides accessible, pre-styled buttons, cards, containers, dialogs, and grid layouts.", tbl_body_style),
            Paragraph("<code>@mui/material</code> imports across all pages", tbl_body_style)
        ],
        [
            Paragraph("Animations", tbl_body_style),
            Paragraph("Framer Motion 9.0", tbl_body_style),
            Paragraph("Smooth micro-animations, page transition fades, and card hover scaling effects.", tbl_body_style),
            Paragraph("<code>MotionCard</code>, <code>MotionPaper</code> in pages", tbl_body_style)
        ],
        [
            Paragraph("Data Visualization", tbl_body_style),
            Paragraph("Chart.js &amp; react-chartjs-2", tbl_body_style),
            Paragraph("Renders crime category breakdown bar charts and risk distribution pie charts.", tbl_body_style),
            Paragraph("<code>src/pages/Dashboard.js</code>", tbl_body_style)
        ],
        [
            Paragraph("Backend Framework", tbl_body_style),
            Paragraph("Flask 3.1 &amp; Flask-CORS", tbl_body_style),
            Paragraph("Lightweight Python web server facilitating REST APIs and cross-origin browser communication.", tbl_body_style),
            Paragraph("<code>ThemeBased Code/app.py</code>", tbl_body_style)
        ],
        [
            Paragraph("Real-Time Communication", tbl_body_style),
            Paragraph("Flask-Sock (WebSockets)", tbl_body_style),
            Paragraph("Bi-directional, low-latency socket streaming for live video frame transfer.", tbl_body_style),
            Paragraph("<code>app.py</code> (`@sock.route('/ws/camera')`)", tbl_body_style)
        ],
        [
            Paragraph("Object Detection", tbl_body_style),
            Paragraph("YOLOv8 Nano (Ultralytics)", tbl_body_style),
            Paragraph("Fast, accurate real-time person bounding box detection (`class=0`).", tbl_body_style),
            Paragraph("<code>video_processor.py</code>, <code>live_camera_processor.py</code>", tbl_body_style)
        ],
        [
            Paragraph("Pose &amp; Gesture Tracking", tbl_body_style),
            Paragraph("MediaPipe Holistic", tbl_body_style),
            Paragraph("Extracts 33 body pose landmarks + 21 hand keypoints to detect SOS distress gestures.", tbl_body_style),
            Paragraph("<code>detect_sos_gesture()</code> in processors", tbl_body_style)
        ],
        [
            Paragraph("Gender Classification", tbl_body_style),
            Paragraph("MobileNetV2 (PyTorch)", tbl_body_style),
            Paragraph("Lightweight convolutional neural network classifying face crops into Male/Female probabilities.", tbl_body_style),
            Paragraph("<code>classify_gender()</code> in processors", tbl_body_style)
        ],
        [
            Paragraph("Geospatial &amp; Geocoding", tbl_body_style),
            Paragraph("Geopy &amp; Folium", tbl_body_style),
            Paragraph("Converts city names to lat/lon coordinates, computes geodesic distances, renders heatmaps.", tbl_body_style),
            Paragraph("<code>app.py</code> (`/api/hotspots/analyze`)", tbl_body_style)
        ],
        [
            Paragraph("Data Processing", tbl_body_style),
            Paragraph("Pandas &amp; NumPy", tbl_body_style),
            Paragraph("Loads Indian crime CSV dataset into memory and computes aggregate crime metrics.", tbl_body_style),
            Paragraph("<code>women-crimedataset-India.csv</code> loading in <code>app.py</code>", tbl_body_style)
        ],
    ]

    tech_table = Table([tech_headers] + tech_rows, colWidths=[100, 110, 154, 140])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: PROJECT IN ONE SIMPLE STORY (PITCHES)
    # =========================================================================
    story.append(Paragraph("3. The HerWatch Story: 30s, 1m, and 3m Elevator Pitches", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("⚡ 30-Second Elevator Pitch (Quick &amp; Memorable)", h2_style))
    pitch_30 = (
        "\"HerWatch is a real-time AI-powered women's safety surveillance system. It uses computer vision models like YOLOv8, "
        "MediaPipe, and MobileNetV2 to automatically detect non-verbal SOS distress gestures and solitary women in high-risk nighttime environments. "
        "It also integrates geospatial crime data via Geopy and Folium to plot interactive crime hotspots. The system streams live video over WebSockets "
        "to a React dashboard, delivering immediate visual and auditory security alerts.\""
    )
    story.append(Paragraph(pitch_30, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("⏱️ 1-Minute Explanation (Balanced Detail)", h2_style))
    pitch_60 = (
        "\"Conventional public surveillance relies heavily on human operators watching CCTV monitors, which leads to fatigue and delayed responses during emergencies. "
        "HerWatch solves this by automating threat detection. We built a full-stack system: the Flask backend processes live video feeds using a multi-model pipeline. "
        "YOLOv8 detects human presence; MediaPipe analyzes 3D body and hand keypoints to recognize distress signals like hand waving or double-raised hands; and MobileNetV2 "
        "performs gender classification to flag lone women in isolated areas between 7 PM and 6 AM. Furthermore, we integrated district-level Indian crime datasets to map risk zones "
        "within a 100km radius. All alerts stream instantly to a React web interface using WebSockets.\""
    )
    story.append(Paragraph(pitch_60, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("🎯 2-3 Minute Comprehensive Deep-Dive Explanation", h2_style))
    pitch_180 = (
        "\"HerWatch is designed as an intelligent situational awareness platform for smart city safety and campus surveillance. "
        "The application addresses two critical security gaps: non-verbal emergency signaling and proactive nocturnal risk monitoring.<br/><br/>"
        "<b>Architecture &amp; Data Flow:</b> The frontend is built with React 18 and Material-UI. When a user opens the Live Camera mode, the browser captures video frames "
        "and transmits them as Base64-encoded JPEG images over a persistent WebSocket connection to our Flask backend.<br/><br/>"
        "<b>AI Pipeline:</b> Upon receiving a frame, the backend invokes our computer vision pipeline: first, YOLOv8n locates persons in the frame. "
        "Second, MediaPipe Holistic extracts 33 pose landmarks and hand keypoints to evaluate geometric distress heuristics—such as raised wrists or side-to-side hand waving over a 2-second sliding window. "
        "Third, face crops from detected bounding boxes are fed into a fine-tuned MobileNetV2 model to classify gender with confidence scoring. If a woman is detected alone at night (19:00 - 06:00) or an SOS gesture occurs, "
        "the frame is annotated with red bounding boxes and warning text, and pushed back over the WebSocket to trigger visual banners and auditory alerts on the frontend.<br/><br/>"
        "<b>Geospatial Intelligence:</b> Additionally, users can search any district in India on the Hotspot Map page. The backend uses Nominatim geocoding to resolve coordinates, calculates geodesic distance against historical crime CSV records using Geopy, "
        "filters locations within 100km, and renders an interactive Folium Leaflet heatmap overlay embedded directly into the React UI.\""
    )
    story.append(Paragraph(pitch_180, body_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 4: END-TO-END ARCHITECTURE & DATA FLOW
    # =========================================================================
    story.append(Paragraph("4. End-to-End Architecture & Startup Sequence", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("System Component Interaction Diagram:", h3_style))
    
    arch_diag = (
        "[ User / Web Browser ]<br/>"
        "       │<br/>"
        "       ▼ (Renders React UI)<br/>"
        "[ React 18 Frontend ] ──(WebSocket /ws/camera)──► [ Flask 3.1 Backend Server ]<br/>"
        "       │                                                  │<br/>"
        "       ├──(REST POST /api/hotspots/analyze)───────────────┤<br/>"
        "       │                                                  ▼<br/>"
        "       │                                       [ AI Computer Vision Engine ]<br/>"
        "       │                                       ├── YOLOv8n (Person BBoxes)<br/>"
        "       │                                       ├── MediaPipe (SOS Gestures)<br/>"
        "       │                                       └── MobileNetV2 (Gender Classifier)<br/>"
        "       │                                                  │<br/>"
        "       │                                                  ▼<br/>"
        "       │                                       [ Geospatial Engine ]<br/>"
        "       │                                       ├── Nominatim (Geocoding)<br/>"
        "       │                                       ├── Geopy (Geodesic Distance)<br/>"
        "       │                                       └── Pandas (Crime CSV Dataset)<br/>"
        "       ▼                                                  │<br/>"
        "[ Annotated Video Canvas &amp; Leaflet Map ] ◄──────────────────┘"
    )
    diag_table = Table([[Paragraph(f"<code>{arch_diag}</code>", code_style)]], colWidths=[504])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Detailed Execution Phases:", h3_style))
    story.append(Paragraph("1. <b>Backend Server Boot:</b> `app.py` runs on port 5001. Loads `women-crimedataset-India.csv` into memory, computes `TOTAL_CRIMES` column, and initializes YOLOv8 (`yolov8n.pt`), MediaPipe Holistic, and MobileNetV2 models.", bullet_style))
    story.append(Paragraph("2. <b>Frontend Client Boot:</b> `App.js` initializes Material-UI theme and React-Router routes. User navigates to `/live-camera` or `/hotspot-map`.", bullet_style))
    story.append(Paragraph("3. <b>WebSocket Video Stream Handshake:</b> `LiveCamera.js` establishes a WebSocket connection to `ws://localhost:5001/ws/camera`. Every 100ms, it captures canvas image bytes, converts to Base64 JPEG, and sends over socket.", bullet_style))
    story.append(Paragraph("4. <b>Frame Inference &amp; Alert Generation:</b> `app.py` receives Base64 frame, decodes to OpenCV BGR matrix, invokes `process_live_camera(frame)`. If SOS gesture or Lone Woman at Night rule triggers, red warning overlays are drawn onto the frame.", bullet_style))
    story.append(Paragraph("5. <b>UI Telemetry Update:</b> Processed annotated Base64 frame and detection metadata JSON are returned over socket, updating the live canvas image and sounding `play_alert_sound()` on frontend.", bullet_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 5: CODE TRACE OF PRIMARY USER FLOWS
    # =========================================================================
    story.append(Paragraph("5. Step-by-Step Code Trace of Primary User Flows", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("Flow 1: Live Webcam Streaming &amp; Real-Time SOS Alerting", h2_style))
    
    flow_headers = [Paragraph("Step", tbl_header_style), Paragraph("File Path", tbl_header_style), Paragraph("Function / Class", tbl_header_style), Paragraph("Exact Operation Executed", tbl_header_style)]
    flow_rows = [
        [
            Paragraph("1", tbl_body_style),
            Paragraph("<code>src/pages/LiveCamera.js</code>", tbl_body_style),
            Paragraph("<code>startCamera()</code>", tbl_body_style),
            Paragraph("Requests browser camera access via <code>navigator.mediaDevices.getUserMedia()</code> and binds video element.", tbl_body_style)
        ],
        [
            Paragraph("2", tbl_body_style),
            Paragraph("<code>src/pages/LiveCamera.js</code>", tbl_body_style),
            Paragraph("<code>WebSocket Connection</code>", tbl_body_style),
            Paragraph("Instantiates <code>new WebSocket('ws://localhost:5001/ws/camera')</code> and attaches <code>onmessage</code> listener.", tbl_body_style)
        ],
        [
            Paragraph("3", tbl_body_style),
            Paragraph("<code>src/pages/LiveCamera.js</code>", tbl_body_style),
            Paragraph("<code>sendFrame()</code>", tbl_body_style),
            Paragraph("Draws current video frame onto hidden HTML5 canvas, exports Base64 string, and sends JSON <code>{frame: base64}</code>.", tbl_body_style)
        ],
        [
            Paragraph("4", tbl_body_style),
            Paragraph("<code>ThemeBased Code/app.py</code>", tbl_body_style),
            Paragraph("<code>ws_camera(ws)</code>", tbl_body_style),
            Paragraph("Receives WebSocket payload, parses JSON, calls <code>process_frame(frame_data)</code>.", tbl_body_style)
        ],
        [
            Paragraph("5", tbl_body_style),
            Paragraph("<code>live_camera_processor.py</code>", tbl_body_style),
            Paragraph("<code>process_live_camera()</code>", tbl_body_style),
            Paragraph("Runs YOLOv8 person detection, MediaPipe Holistic keypoint extraction, and MobileNetV2 gender scoring.", tbl_body_style)
        ],
        [
            Paragraph("6", tbl_body_style),
            Paragraph("<code>live_camera_processor.py</code>", tbl_body_style),
            Paragraph("<code>detect_sos_gesture()</code>", tbl_body_style),
            Paragraph("Calculates hand landmark coordinates. If wave count &gt;= 2 or wrists above wrist line, adds <code>'SOS Wave Detected'</code> to alert list.", tbl_body_style)
        ],
        [
            Paragraph("7", tbl_body_style),
            Paragraph("<code>live_camera_processor.py</code>", tbl_body_style),
            Paragraph("<code>show_alert()</code>", tbl_body_style),
            Paragraph("Draws red border rectangle `cv2.rectangle` and red warning text banner on OpenCV frame.", tbl_body_style)
        ],
        [
            Paragraph("8", tbl_body_style),
            Paragraph("<code>src/pages/LiveCamera.js</code>", tbl_body_style),
            Paragraph("<code>ws.onmessage</code>", tbl_body_style),
            Paragraph("Receives annotated frame Base64, updates React `processedFrame` state, and renders red alert alert banner in UI.", tbl_body_style)
        ],
    ]

    flow_table = Table([flow_headers] + flow_rows, colWidths=[30, 130, 130, 214])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(flow_table)

    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: FRONTEND DEEP EXPLANATION (REACT.JS)
    # =========================================================================
    story.append(Paragraph("6. Frontend Architecture Deep Dive (React 18)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "The frontend is a single-page React 18 application initialized via `react-scripts`. It manages routing via "
        "`react-router-dom` (v6) and implements styling using Material-UI theme providers and Framer Motion.",
        body_style
    ))

    story.append(Paragraph("Core Pages Breakdown:", h3_style))

    # Detailed file breakdowns
    fe_files = [
        ("src/App.js", "Main Routing & Theme Provider", "Creates custom MUI theme with dark blue (`#1a237e`) primary color and pink secondary (`#f50057`). Defines `BrowserRouter`, `Routes`, and public/private layout routes. Contains `PrivateRoute` mock wrapper (`isAuthenticated = true`)."),
        ("src/components/Navbar.js", "Navigation Header Bar", "Renders responsive top navigation bar containing HerWatch logo icon, page links (Home, Dashboard, Live Camera, Video Mode, Hotspot Map, About), and profile menu button."),
        ("src/pages/LiveCamera.js", "WebSocket Webcam Streaming", "Core real-time interface. Uses `useRef` for WebSocket instance and HTML5 video/canvas elements. Maintains `isStreaming`, `cameraList`, `alertHistory`, and `fps` states."),
        ("src/pages/HotspotMap.js", "Geospatial Map Search", "Fetches `/api/health` on mount to verify backend connectivity. Maintains `location` input, `currentLocation` GPS coords, and renders Folium HTML map within an iframe container."),
        ("src/pages/VideoMode.js", "Recorded Video File Analyzer", "Provides drag-and-drop file upload interface for MP4/AVI files. Sends `FormData` payload to `/analyze_video` endpoint and displays detection timeline log."),
        ("src/pages/Dashboard.js", "Crime Statistics Charts", "Integrates `react-chartjs-2` to display crime category distribution bar charts and high-risk hour frequency area charts based on aggregated dataset statistics.")
    ]

    for fname, fpurpose, fdetail in fe_files:
        story.append(Paragraph(f"<b>File:</b> <code>{fname}</code> — <i>{fpurpose}</i>", h3_style))
        story.append(Paragraph(f"<b>Implementation Details:</b> {fdetail}", body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: BACKEND DEEP EXPLANATION (FLASK & API)
    # =========================================================================
    story.append(Paragraph("7. Backend & API Endpoint Specification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "The Flask backend server (`app.py`) runs on port `5001`. It uses `flask-cors` to enable cross-origin requests and "
        "`flask-sock` for WebSocket support.",
        body_style
    ))

    api_headers2 = [Paragraph("HTTP / WS", tbl_header_style), Paragraph("Endpoint Route", tbl_header_style), Paragraph("Input Request", tbl_header_style), Paragraph("Processing & Response Output", tbl_header_style)]
    api_rows2 = [
        [
            Paragraph("<code>GET</code>", tbl_body_style),
            Paragraph("<code>/api/health</code>", tbl_body_style),
            Paragraph("None", tbl_body_style),
            Paragraph("Checks backend server status. Returns <code>{\"status\": \"ok\", \"message\": \"API is running\"}</code>.", tbl_body_style)
        ],
        [
            Paragraph("<code>POST</code>", tbl_body_style),
            Paragraph("<code>/api/hotspots/analyze</code>", tbl_body_style),
            Paragraph("JSON: <code>{location: \"Delhi\"}</code> or lat/lon", tbl_body_style),
            Paragraph("Invokes Geopy Nominatim, filters crime dataset within 100km radius, generates Folium HTML map, returns map iframe source.", tbl_body_style)
        ],
        [
            Paragraph("<code>POST</code>", tbl_body_style),
            Paragraph("<code>/analyze_video</code>", tbl_body_style),
            Paragraph("Form Data: Video file (`.mp4`, `.avi`)", tbl_body_style),
            Paragraph("Processes uploaded video frame-by-frame via <code>video_processor.py</code>, exports annotated video file, returns detection summary JSON.", tbl_body_style)
        ],
        [
            Paragraph("<code>GET</code>", tbl_body_style),
            Paragraph("<code>/api/live-camera/list</code>", tbl_body_style),
            Paragraph("None", tbl_body_style),
            Paragraph("Probes local hardware video indices (`cv2.VideoCapture(i)`) and returns list of available connected camera devices.", tbl_body_style)
        ],
        [
            Paragraph("<code>WebSocket</code>", tbl_body_style),
            Paragraph("<code>/ws/camera</code>", tbl_body_style),
            Paragraph("JSON string: <code>{frame: Base64}</code>", tbl_body_style),
            Paragraph("Executes <code>process_live_camera(frame)</code>. Pushes annotated Base64 JPEG frame and alert metadata back over socket connection.", tbl_body_style)
        ],
    ]

    api_table2 = Table([api_headers2] + api_rows2, colWidths=[70, 140, 110, 184])
    api_table2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(api_table2)

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 8: DATABASE & GEOSPATIAL DATA LAYER
    # =========================================================================
    story.append(Paragraph("8. Database & Data Storage Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "<b>Important Interview Clarification:</b> The current HerWatch codebase does <b>NOT</b> utilize a traditional relational (SQL) or document (NoSQL) database. "
        "Instead, it relies on an in-memory Pandas DataFrame loaded from a static CSV dataset: <code>women-crimedataset-India.csv</code>.",
        body_style
    ))

    story.append(Paragraph("Dataset & In-Memory Data Pipeline:", h3_style))
    story.append(Paragraph("• <b>File Schema:</b> Contains state, district, latitude, longitude, and 12 crime category columns (Rape, Assault, Kidnapping, Dowry Deaths, Cruelty by Husband, etc.).", bullet_style))
    story.append(Paragraph("• <b>Initialization:</b> On `app.py` startup, Pandas reads the CSV (`pd.read_csv('women-crimedataset-India.csv')`) and dynamically computes the `TOTAL_CRIMES` column by summing columns 3 through 14.", bullet_style))
    story.append(Paragraph("• <b>Geodesic Distance Filtering:</b> When a user submits a location query, Geopy calculates the distance from the target coordinates to every row in the DataFrame using `geodesic((user_lat, user_lon), (row_lat, row_lon)).kilometers`.", bullet_style))
    story.append(Paragraph("• <b>Thresholding:</b> Rows with distance `> 100km` are filtered out, and the remaining nearby hotspots are sorted ascending by distance to render Folium risk circles.", bullet_style))

    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 9: AUTHENTICATION, SECURITY & CORS
    # =========================================================================
    story.append(Paragraph("9. Authentication & Security Implementation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "<b>Authentication Status:</b> The frontend includes UI forms for Login (`Login.js`) and Registration (`Register.js`), as well as a "
        "`PrivateRoute` wrapper in `App.js`. However, backend JWT token generation or session persistence is currently <b>mocked</b> (`isAuthenticated = true`). "
        "When asked in an interview, clearly explain that the UI forms are built for client-side demonstration, with full JWT/OAuth integration planned for future iterations.",
        body_style
    ))

    story.append(Paragraph("Security Mechanisms Currently Implemented:", h3_style))
    story.append(Paragraph("• <b>CORS (Cross-Origin Resource Sharing):</b> `CORS(app, resources={r'/*': {'origins': '*'}})` is configured in `app.py` to allow the React frontend running on port 3000 to make HTTP and WebSocket requests to port 5001.", bullet_style))
    story.append(Paragraph("• <b>Input Sanitization & Geocoding Retry:</b> `geocode_with_retry()` strips whitespace, appends ', India' to input location strings, and enforces timeout limits to prevent API abuse or hang issues.", bullet_style))
    story.append(Paragraph("• <b>WebSocket Buffer Limit:</b> `frame_queue = queue.Queue(maxsize=10)` caps incoming video frame buffering to prevent memory overflow attacks.", bullet_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 10: AI / MACHINE LEARNING PIPELINE
    # =========================================================================
    story.append(Paragraph("10. AI / Machine Learning Computer Vision Pipeline", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "HerWatch executes an ensemble of 3 distinct machine learning models operating sequentially on incoming video frames:",
        body_style
    ))

    # Models detail
    story.append(Paragraph("1. YOLOv8 Nano (Person Detection)", h2_style))
    story.append(Paragraph("• <b>Architecture:</b> Ultralytics YOLOv8n (Pretrained on COCO dataset, 3.2M parameters).", bullet_style))
    story.append(Paragraph("• <b>Role:</b> Detects human objects in the frame (`class_id == 0`). Filters out detections with confidence `< 0.40`.", bullet_style))

    story.append(Paragraph("2. MediaPipe Holistic (SOS Distress Gesture Tracking)", h2_style))
    story.append(Paragraph("• <b>Architecture:</b> Google MediaPipe Holistic Solution (Combines PoseLandmarker and HandLandmarker).", bullet_style))
    story.append(Paragraph("• <b>Role:</b> Extracts 33 body pose landmarks and 21 3D hand keypoints per hand. Evaluates heuristic rules:", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;- <i>Raised Hand:</i> `Middle_Finger_Tip.y < Wrist.y` and `Wrist.y < 0.5`.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;- <i>Hand Waving:</i> `|Middle_Finger_Tip.x - Wrist.x| > 0.15` over sliding time window.", bullet_style))

    story.append(Paragraph("3. MobileNetV2 (Gender Classification)", h2_style))
    story.append(Paragraph("• <b>Architecture:</b> PyTorch `torchvision.models.mobilenet_v2(pretrained=True)`.", bullet_style))
    story.append(Paragraph("• <b>Role:</b> Crops upper 60% of detected person bounding box (head/torso region), resizes to `224x224 RGB`, normalizes tensor values, and computes Softmax probability output (`Female` vs `Male`).", bullet_style))

    story.append(Paragraph("4. Nocturnal Lone Woman Decision Rule", h2_style))
    story.append(Paragraph("• <b>Condition:</b> `is_nighttime()` (Current hour `>= 19` or `<= 6`), `Total_Persons == 1`, `Gender == 'Female'`, and `Confidence >= 0.60`. Triggers high-priority <b>LONE WOMAN AT NIGHT</b> emergency alert.", bullet_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 11: IMPORTANT SOFTWARE ENGINEERING CONCEPTS
    # =========================================================================
    story.append(Paragraph("11. Important Software Engineering Concepts Used", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    concepts = [
        ("REST API Architecture", "Decouples frontend UI from backend business logic using standard HTTP verbs (GET, POST) and JSON format payloads."),
        ("WebSocket Protocol", "Full-duplex, persistent TCP connection enabling low-latency real-time video frame streaming without HTTP polling overhead."),
        ("Inference Mode (`torch.no_grad()`)", "Disables PyTorch gradient calculation autograd engine during MobileNetV2 evaluation, significantly reducing GPU/CPU memory consumption."),
        ("React State & Side Effects (`useState`, `useEffect`)", "Manages dynamic UI state (camera streaming toggle, alert arrays, map URL) and handles component lifecycle events."),
        ("React References (`useRef`)", "Persists mutable DOM references (HTML5 video/canvas elements) and WebSocket instances across component re-renders without causing re-render loops."),
        ("Multithreading & Frame Queues (`queue.Queue`)", "Prevents UI thread blocking during video processing by isolating frame reading and model inference into separate worker queues."),
        ("Geodesic Coordinate Calculations", "Uses great-circle distance mathematics to compute exact spherical surface distance between latitude/longitude pairs.")
    ]

    for ctitle, cdesc in concepts:
        story.append(Paragraph(f"• <b>{ctitle}:</b> {cdesc}", bullet_style))

    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 12: RANKED FILE PRIORITY MATRIX
    # =========================================================================
    story.append(Paragraph("12. Ranked File Priority Matrix for Interviews", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("🥇 Priority 1: MUST KNOW (Core Core Logic)", h2_style))
    p1_files = [
        ("ThemeBased Code/app.py", "Backend entry point, REST routes, WebSocket handler, and Pandas dataset loader."),
        ("ThemeBased Code/live_camera_processor.py", "Core AI processing engine executing YOLOv8, MediaPipe, MobileNetV2, and alert overlay rendering."),
        ("sos-detection-frontend/src/pages/LiveCamera.js", "Primary real-time frontend page managing webcam stream, WebSockets, canvas encoding, and UI alert badges.")
    ]
    for pf, pd in p1_files:
        story.append(Paragraph(f"• <b><code>{pf}</code></b>: {pd}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("🥈 Priority 2: SHOULD KNOW (Supporting Business Logic)", h2_style))
    p2_files = [
        ("ThemeBased Code/video_processor.py", "Recorded video batch processing script for uploaded files."),
        ("sos-detection-frontend/src/pages/HotspotMap.js", "Geospatial crime search interface integrating Geopy API and Folium iframe."),
        ("sos-detection-frontend/src/App.js", "Main React routing configuration, Material-UI theme setup, and PrivateRoute wrapper.")
    ]
    for pf, pd in p2_files:
        story.append(Paragraph(f"• <b><code>{pf}</code></b>: {pd}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("🥉 Priority 3: NICE TO KNOW (Utilities & Layout)", h2_style))
    p3_files = [
        ("sos-detection-frontend/src/pages/Dashboard.js", "Chart.js visualization charts for crime category statistics."),
        ("ThemeBased Code/requirements.txt", "Python dependency manifest listing Flask, OpenCV, MediaPipe, PyTorch, Ultralytics."),
        ("sos-detection-frontend/package.json", "Node manifest detailing React 18, Material-UI, Framer Motion, and start/build scripts.")
    ]
    for pf, pd in p3_files:
        story.append(Paragraph(f"• <b><code>{pf}</code></b>: {pd}", bullet_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 13: 50 REALISTIC TECHNICAL INTERVIEW QUESTIONS & ANSWERS
    # =========================================================================
    story.append(Paragraph("13. 50+ Realistic Technical Interview Questions & Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    qa_list = [
        # Basic
        ("Q1: What is HerWatch and what problem does it solve?",
         "HerWatch is an AI-driven women's safety surveillance system. It solves the problem of passive CCTV monitoring by automatically detecting non-verbal SOS gestures, lone women at night, and mapping crime risk zones in real time.",
         "In `live_camera_processor.py`, models process video feeds autonomously and trigger instant alerts without requiring manual human observation."),
        
        ("Q2: Who are the target end-users for this project?",
         "Smart city municipal authorities, campus security personnel, transit authorities, and law enforcement agencies responsible for public surveillance.",
         "The React dashboard provides real-time security alerts and crime hotspot heatmaps tailored for security command centers."),

        ("Q3: What are the main features implemented in your codebase?",
         "SOS Gesture Detection, Lone Woman Detection at Night, Geospatial Crime Hotspot Mapping, Dual Mode (Live Webcam WebSocket + Recorded Video File Upload), and Crime Analytics Dashboard.",
         "Features are mapped directly across `LiveCamera.js`, `VideoMode.js`, `HotspotMap.js`, and `app.py`."),

        ("Q4: Is HerWatch a desktop application or a web application?",
         "It is a full-stack web application with a React single-page frontend and a Python Flask backend server communicating over HTTP and WebSockets.",
         "Frontend runs on port 3000 (`npm start`) and backend runs on port 5001 (`python app.py`)."),

        ("Q5: What happens if no webcam is connected to the computer?",
         "`/api/live-camera/list` probes video indices via OpenCV. If no cameras are found, `LiveCamera.js` displays an alert informing the user to connect a video device or switch to Video Mode file upload.",
         "Handled via `cv2.VideoCapture(i).isOpened()` in `live_camera_processor.py`."),

        # Frontend
        ("Q6: How is routing handled in your React frontend?",
         "Using `react-router-dom` (v6) in `App.js`. Routes like `/live-camera`, `/hotspot-map`, and `/dashboard` are wrapped inside a main `<Layout />` route containing the Navbar.",
         "See `<Route path='/' element={<Layout />}>` in `App.js`."),

        ("Q7: Why did you use Material-UI (MUI v5) for the frontend?",
         "Material-UI provides accessible, pre-built design components like `Box`, `Container`, `Card`, `Dialog`, and `Typography`, allowing rapid assembly of a polished, responsive dashboard.",
         "Imported across all pages in `sos-detection-frontend/src/pages/`."),

        ("Q8: How does Framer Motion enhance your user interface?",
         "Framer Motion provides smooth micro-animations, such as element fade-ins and subtle hover scaling on dashboard cards (`MotionCard`, `MotionPaper`), giving the app a modern aesthetic.",
         "See `motion(Card)` wrappers in `HotspotMap.js` and `Login.js`."),

        ("Q9: What role does HTML5 Canvas play in LiveCamera.js?",
         "The canvas is used as an off-screen image buffer. It draws the current `<video>` frame and exports a Base64 encoded JPEG string (`canvas.toDataURL('image/jpeg')`) to send over WebSocket.",
         "Implemented inside `sendFrame()` in `LiveCamera.js`."),

        ("Q10: How do you handle component lifecycle and cleanup in React?",
         "Using the `useEffect` hook with clean-up functions. For example, when `LiveCamera.js` unmounts, its `useEffect` cleanup closes the WebSocket connection and stops webcam media tracks.",
         "See `return () => { ws.close(); track.stop(); }` in `LiveCamera.js`."),

        # Backend
        ("Q11: Why did you choose Flask instead of Django for the backend?",
         "Flask is lightweight, unopinionated, and fast to set up. It integrates seamlessly with PyTorch, OpenCV, and WebSockets (`flask-sock`) without the overhead of Django's heavy ORM and administrative boilerplate.",
         "Implemented in a single clean entry file `ThemeBased Code/app.py`."),

        ("Q12: How are Cross-Origin Resource Sharing (CORS) issues handled?",
         "Using `flask-cors`. We initialize `CORS(app, resources={r'/*': {'origins': '*'}})` to permit request headers from the React frontend running on port 3000.",
         "See line 25 in `ThemeBased Code/app.py`."),

        ("Q13: What endpoint verifies backend availability?",
         "`GET /api/health`. It returns HTTP status 200 with JSON payload `{\"status\": \"ok\", \"message\": \"API is running\"}`.",
         "`HotspotMap.js` calls this endpoint on mount to verify backend health."),

        ("Q14: How does Flask serve the interactive Folium HTML map?",
         "The endpoint `/api/hotspots/analyze` generates an HTML file (`crime_hotspot_map.html`) and returns the HTML string or serves it directly for iframe embedding.",
         "See `folium.Map().save('crime_hotspot_map.html')` in `app.py`."),

        ("Q15: How are video files uploaded and processed in VideoMode?",
         "The frontend posts `FormData` containing the file to `/analyze_video`. `app.py` saves the file to `uploads/`, invokes `process_video_combined()`, and returns the annotated output video URL.",
         "See `@app.route('/analyze_video', methods=['POST'])` in `app.py`."),

        # AI / ML
        ("Q16: Which model detects human presence in video frames?",
         "Ultralytics YOLOv8 Nano (`yolov8n.pt`). It predicts bounding box coordinates and object class IDs (`class_id == 0` for person).",
         "`yolo_model = YOLO('yolov8n.pt')` in `live_camera_processor.py`."),

        ("Q17: Why did you use MediaPipe for gesture detection?",
         "MediaPipe Holistic provides high-fidelity 3D landmark tracking for 33 body pose points and 21 hand points per hand at sub-50ms latency, enabling accurate spatial rule checking without training custom models.",
         "`mp_holistic.Holistic(...)` in `live_camera_processor.py`."),

        ("Q18: How is the 'Raised Hand' gesture mathematically calculated?",
         "By comparing landmark Y-coordinates: `Middle_Finger_Tip.y < Wrist.y` and `Wrist.y < 0.5`. In normalized image coordinates, smaller Y values indicate higher vertical position.",
         "Implemented in `detect_raised_hand()` in `live_camera_processor.py`."),

        ("Q19: How does the system detect hand waving?",
         "It tracks horizontal displacement `|Middle_Finger_Tip.x - Wrist.x| > 0.15` and vertical displacement `> 0.25` across frames over a sliding 2.0-second time window.",
         "Implemented in `detect_wave()` in `live_camera_processor.py`."),

        ("Q20: How does MobileNetV2 classify gender?",
         "The face/torso region (upper 60% of person box) is cropped, resized to `224x224`, normalized into a float tensor, and passed to MobileNetV2. Softmax outputs male vs female probability.",
         "Implemented in `classify_gender()` in `live_camera_processor.py`."),

        ("Q21: What logic defines a 'Lone Woman at Night' emergency alert?",
         "Four simultaneous conditions: `is_nighttime() == True` (19:00 to 06:00), `Total_Persons == 1`, `Gender == 'Female'`, and `Gender_Confidence >= 0.60`.",
         "Evaluated inside `process_live_camera()` in `live_camera_processor.py`."),

        ("Q22: Why did you set `torch.no_grad()` during MobileNetV2 inference?",
         "Disabling autograd gradient tracking reduces CPU/GPU memory allocation and accelerates inference speed during model evaluation.",
         "See `with torch.no_grad():` in `classify_gender()`."),

        ("Q23: How does frame skipping improve real-time performance?",
         "Processing every frame slows down FPS. Setting `FRAME_SKIP = 3` skips inference on 2 out of 3 frames, maintaining smooth 30 FPS video rendering.",
         "See `FRAME_SKIP = 3` in `live_camera_processor.py`."),

        # Data & Geospatial
        ("Q24: What dataset is used for crime hotspot mapping?",
         "`women-crimedataset-India.csv`. It contains district-level Indian government records for 12 crime categories.",
         "Loaded into Pandas DataFrame `df` on `app.py` server startup."),

        ("Q25: How is total crime calculated if not present in the CSV?",
         "Pandas sums columns 3 through 14 across rows: `df['TOTAL_CRIMES'] = df[crime_columns].sum(axis=1)`.",
         "Executed during dataset loading in `app.py`."),

        ("Q26: How does Geopy convert district names into coordinates?",
         "Using `Nominatim(user_agent='herwatch')`. The function `geocode_with_retry()` sends the location string to Nominatim API and receives latitude and longitude.",
         "Implemented in `app.py` lines 61-78."),

        ("Q27: What distance metric is used to find nearby hotspots?",
         "Geodesic distance calculated via `geodesic((user_lat, user_lon), (row['Latitude'], row['Longitude'])).kilometers`.",
         "Filters locations within `MAX_DISTANCE_KM = 100` in `app.py`."),

        ("Q28: How are risk levels represented visually on the Folium map?",
         "Red circle markers for High Risk (>1000 total crimes), Orange for Medium Risk, and Green for Low Risk.",
         "Rendered via `folium.CircleMarker()` in `app.py`."),

        # Architecture & Flow
        ("Q29: What protocol is used for live video streaming?",
         "WebSockets (`ws://localhost:5001/ws/camera`) via `flask-sock` and native browser WebSocket API.",
         "Enables full-duplex, low-latency streaming without HTTP polling overhead."),

        ("Q30: How are annotated frames returned to the frontend?",
         "OpenCV draws red boxes and alert text onto the frame matrix. The frame is encoded to JPEG Base64 and sent over the WebSocket as a JSON payload.",
         "Processed in `ws_camera()` in `app.py`."),

        ("Q31: What happens if the WebSocket connection drops unexpectedly?",
         "`LiveCamera.js` detects `ws.onclose`, sets streaming state to false, and displays an error alert prompting the user to reconnect.",
         "Handled in `startCamera()` error block in `LiveCamera.js`."),

        ("Q32: How does the frontend sound audio alerts?",
         "When an alert is present in the received socket payload, `LiveCamera.js` invokes an HTML5 Audio object to play a warning alert beep.",
         "Implemented in `playAlertSound()` in `LiveCamera.js`."),

        # Security & Auth
        ("Q33: How is user login currently structured in the codebase?",
         "Login UI is built in `Login.js` with form state tracking. Form submission redirects to `/dashboard`. Authentication logic is client-side mocked.",
         "See `handleSubmit` in `Login.js`."),

        ("Q34: How does PrivateRoute protect frontend routes?",
         "In `App.js`, `PrivateRoute` checks `isAuthenticated`. If true, it renders child components; if false, it redirects to `/login`.",
         "Currently mocked with `const isAuthenticated = true` in `App.js`."),

        ("Q35: How would you secure API endpoints with JWT tokens?",
         "Implement `flask-jwt-extended`. Upon valid login at `/api/login`, return a signed JWT access token. Secure endpoints with `@jwt_required()` decorator.",
         "Planned enhancement for production deployment."),

        # Troubleshooting & Real Issues
        ("Q36: What issue occurred with NumPy 2.x and how was it resolved?",
         "PyTorch and OpenCV were compiled against NumPy 1.x ABI. Installing NumPy 2.2.6 caused a runtime crash (`Failed to initialize NumPy`). Resolved by installing `numpy==1.26.4` (`numpy<2`).",
         "Resolved in virtual environment (`venv`)."),

        ("Q37: Why did `npm start` fail on macOS initially?",
         "`package.json` contained Windows CMD syntax (`set NODE_OPTIONS=... && react-scripts start`). Updated to standard cross-platform syntax (`NODE_OPTIONS=... react-scripts start`).",
         "Fixed in `sos-detection-frontend/package.json`."),

        ("Q38: How do you prevent memory leaks when processing video feeds?",
         "By limiting queue sizes (`queue.Queue(maxsize=10)`), releasing OpenCV capture objects (`cap.release()`), and closing WebSockets on component unmount.",
         "Implemented across `app.py` and `LiveCamera.js`."),

        ("Q39: What happens if Geopy Nominatim times out?",
         "`geocode_with_retry()` catches `GeocoderTimedOut` and retries up to 3 times with exponential backoff delays.",
         "Implemented in `app.py` line 61."),

        ("Q40: How do you verify backend API health before rendering UI components?",
         "`HotspotMap.js` issues a `fetch('/api/health')` request in `useEffect()`. If status is 200, it enables search inputs; otherwise it displays a backend error alert.",
         "See `checkApiStatus()` in `HotspotMap.js`."),

        # Difficult & Code Level
        ("Q41: Why use YOLOv8 Nano instead of YOLOv8 Large?",
         "YOLOv8 Nano has only 3.2 million parameters, offering inference speeds over 60 FPS on CPU, which is crucial for real-time video processing.",
         "Model loaded via `YOLO('yolov8n.pt')`."),

        ("Q42: What is the purpose of `cv2.cvtColor(img, cv2.COLOR_RGB2BGR)`?",
         "PIL and browser canvas images use RGB color order, whereas OpenCV processes images in BGR format. Conversion is required for correct color representation.",
         "See `base64_to_cv2()` in `app.py`."),

        ("Q43: What is the role of `queue.Queue(maxsize=10)` in `app.py`?",
         "It buffers incoming WebSocket frames to prevent memory exhaustion if model inference takes slightly longer than frame capture rate.",
         "Global variable in `app.py`."),

        ("Q44: How does `useRef` differ from `useState` in `LiveCamera.js`?",
         "`useState` causes component re-renders when updated. `useRef` holds mutable references (like the WebSocket instance `wsRef`) without causing unnecessary re-renders.",
         "See `const wsRef = useRef(null)` in `LiveCamera.js`."),

        ("Q45: How would you scale this application for 10,000 concurrent cameras?",
         "Offload video stream ingestion to WebRTC / RTSP media servers, deploy Flask backend across Kubernetes pods with GPU acceleration, and use Redis for WebSocket message pub/sub.",
         "Recommended scaling architecture."),

        ("Q46: Why is dataset loading performed inside a `try-except` block at startup?",
         "To prevent server crash if `women-crimedataset-India.csv` is missing or corrupted. If loading fails, `df` is set to `None` and relevant endpoints return HTTP 500 error messages.",
         "See lines 35-43 in `app.py`."),

        ("Q47: How does `React.memo` or component optimization help in this dashboard?",
         "Prevents unnecessary re-renders of static UI cards and chart canvases when video frame state updates rapidly.",
         "Performance optimization technique."),

        ("Q48: What is the benefit of serving Folium maps via iframe in React?",
         "Folium outputs raw HTML/JavaScript leaflet code. Embedding via `<iframe>` isolates external Leaflet scripts and styles from conflicting with React DOM.",
         "Implemented in `HotspotMap.js`."),

        ("Q49: What metric determines if a gesture counts as SOS hand waving?",
         "Horizontal wrist-to-finger tip displacement crossing the `0.15` threshold at least `MIN_WAVE_COUNT = 2` times within a 2-second interval.",
         "Evaluated in `detect_sos_gesture()`."),

        ("Q50: How do you explain your personal contribution to this project?",
         "\"I worked on integrating the multi-model AI pipeline (YOLOv8, MediaPipe, MobileNetV2) into a unified Flask WebSocket backend, fixing environment compatibility issues, and connecting real-time telemetry to the React dashboard UI.\"",
         "Accurate, professional interview answer.")
    ]

    for q_title, q_ans, q_ex in qa_list:
        story.append(Paragraph(f"<b>{q_title}</b>", h3_style))
        story.append(Paragraph(f"<b>Answer:</b> {q_ans}", body_style))
        story.append(Paragraph(f"<i>Project Code Context: {q_ex}</i>", callout_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 14: LINE-BY-LINE "EXPLAIN THIS CODE" SNIPPETS
    # =========================================================================
    story.append(Paragraph("14. \"Explain This Code\" — Crucial Code Snippets", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    snippets = [
        ("Snippet 1: Base64 to OpenCV BGR Conversion",
         "ThemeBased Code/app.py",
         "def base64_to_cv2(base64_string):\n"
         "    img_data = base64.b64decode(base64_string.split(',')[1])\n"
         "    img = Image.open(io.BytesIO(img_data))\n"
         "    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)",
         "Splits the Data URL header, decodes Base64 bytes into PIL Image, converts PIL matrix to NumPy array, and shifts color space from RGB to OpenCV BGR format."),

        ("Snippet 2: MobileNetV2 Gender Inference",
         "ThemeBased Code/live_camera_processor.py",
         "face_img = cv2.resize(face_img, (224, 224))\n"
         "face_tensor = torch.tensor(face_img, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0) / 255.0\n"
         "with torch.no_grad():\n"
         "    output = gender_model(face_tensor)\n"
         "pred_idx = output.argmax().item()\n"
         "confidence = torch.softmax(output, dim=1)[0][pred_idx].item()",
         "Resizes crop to 224x224, converts HWC image to CHW PyTorch tensor, normalizes pixel values to [0,1], disables gradient tracking, passes tensor into MobileNetV2, and computes Softmax confidence."),

        ("Snippet 3: Geodesic Crime Hotspot Calculation",
         "ThemeBased Code/app.py",
         "df_copy['distance'] = df_copy.apply(\n"
         "    lambda row: geodesic((user_lat, user_lon), (row['Latitude'], row['Longitude'])).kilometers\n"
         "    if not pd.isna(row['Latitude']) else float('inf'), axis=1\n"
         ")\n"
         "nearby_hotspots = df_copy[df_copy['distance'] <= 100].sort_values(by='distance')",
         "Applies Geopy geodesic spherical formula row-by-row against user coordinates, filters locations within 100km, and sorts hotspots in ascending order of proximity."),

        ("Snippet 4: WebSocket Real-Time Frame Handler",
         "ThemeBased Code/app.py",
         "@sock.route('/ws/camera')\n"
         "def ws_camera(ws):\n"
         "    while True:\n"
         "        data = ws.receive()\n"
         "        frame_data = json.loads(data).get('frame')\n"
         "        detections = process_frame(frame_data)\n"
         "        ws.send(json.dumps(detections))",
         "Establishes persistent full-duplex WebSocket connection. Continuously receives JSON frame payloads, processes detections, and sends annotated Base64 response back to React client.")
    ]

    for stitle, spath, scode, sexp in snippets:
        story.append(Paragraph(f"<b>{stitle}</b> (<code>{spath}</code>)", h3_style))
        formatted_code = scode.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>')
        s_tbl = Table([[Paragraph(f"<code>{formatted_code}</code>", code_style)]], colWidths=[504])
        s_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
            ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(s_tbl)
        story.append(Paragraph(f"<b>Explanation:</b> {sexp}", body_style))
        story.append(Spacer(1, 8))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 15: REAL DEBUGGING CASE STUDIES
    # =========================================================================
    story.append(Paragraph("15. Real Debugging Case Studies & Fixes", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("Case Study 1: NumPy 2.x PyTorch C-ABI Crash", h2_style))
    story.append(Paragraph("• <b>Problem:</b> Starting Flask server (`app.py`) produced `UserWarning: Failed to initialize NumPy: _ARRAY_API not found` followed by PyTorch C-extension initialization crash.", bullet_style))
    story.append(Paragraph("• <b>Root Cause:</b> PyTorch 2.2.2 and OpenCV 4.13 installed in `venv` were compiled against NumPy 1.x C-ABI specifications. NumPy automatically upgraded to version 2.2.6, breaking backwards compatibility.", bullet_style))
    story.append(Paragraph("• <b>Resolution:</b> Downgraded virtual environment NumPy package to version 1.26.4 (`pip install 'numpy<2'`). Verified backend boot success.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Case Study 2: Windows `set` Command Failure on macOS", h2_style))
    story.append(Paragraph("• <b>Problem:</b> Running `npm start` in `sos-detection-frontend` failed on macOS zsh shell.", bullet_style))
    story.append(Paragraph("• <b>Root Cause:</b> `package.json` contained Windows CMD syntax: `\"start\": \"set NODE_OPTIONS=... && react-scripts start\"`.", bullet_style))
    story.append(Paragraph("• <b>Resolution:</b> Modified `package.json` scripts to standard cross-platform format: `\"start\": \"NODE_OPTIONS=--openssl-legacy-provider react-scripts start\"`.", bullet_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 16: ULTIMATE 5-MINUTE PRE-INTERVIEW CHEAT SHEET
    # =========================================================================
    story.append(Paragraph("16. Ultimate 5-Minute Pre-Interview Cheat Sheet", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    cs_box = (
        "<b>📌 HerWatch in 5 Lines:</b><br/>"
        "1. HerWatch is a real-time AI women's safety surveillance system built with React and Flask.<br/>"
        "2. Uses YOLOv8 for person detection, MediaPipe for SOS gesture recognition, and MobileNetV2 for gender classification.<br/>"
        "3. Triggers emergency alerts for non-verbal distress signals and solitary women at night (19:00 - 06:00).<br/>"
        "4. Integrates Geopy and Folium to plot interactive 100km crime hotspot heatmaps from Indian crime datasets.<br/>"
        "5. Streams live video frames over WebSockets (`/ws/camera`) to deliver sub-second dashboard alerts.<br/><br/>"
        "<b>🛠️ Tech Stack in 5 Lines:</b><br/>"
        "• Frontend: React 18, Material-UI, Framer Motion, Chart.js<br/>"
        "• Backend: Flask 3.1, Flask-CORS, Flask-Sock (WebSockets)<br/>"
        "• Computer Vision: YOLOv8n, MediaPipe Holistic, MobileNetV2 (PyTorch)<br/>"
        "• Data &amp; Geospatial: Pandas, Geopy (Nominatim &amp; Geodesic), Folium Leaflet<br/>"
        "• Ports: Frontend = 3000, Backend = 5001<br/><br/>"
        "<b>🔑 Top 5 Commands to Remember:</b><br/>"
        "1. Backend Run: <code>cd \"ThemeBased Code\" &amp;&amp; source venv/bin/activate &amp;&amp; python app.py</code><br/>"
        "2. Frontend Run: <code>cd \"ThemeBased Code/sos-detection-frontend\" &amp;&amp; npm start</code><br/>"
        "3. Health Check: <code>curl http://localhost:5001/api/health</code><br/>"
        "4. WebSocket URL: <code>ws://localhost:5001/ws/camera</code><br/>"
        "5. Crime Dataset File: <code>women-crimedataset-India.csv</code>"
    )

    cs_table = Table([[Paragraph(cs_box, body_style)]], colWidths=[504])
    cs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")), # Amber 100
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(cs_table)

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=TEXT_MUTED, spaceBefore=10, spaceAfter=15))
    story.append(Paragraph("<i>End of Complete Project Interview Preparation Guide — HerWatch Project.</i>", ParagraphStyle('EndMeta', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=TEXT_MUTED)))

    # Render PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Complete Interview Guide PDF generated at: {output_filename}")

if __name__ == '__main__':
    target_pdf = "/Users/spurthinaveli/Desktop/Herwatch/HerWatch_Complete_Interview_Preparation_Guide.pdf"
    build_interview_preparation_pdf(target_pdf)
