import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
from modules.data_input import DataInputManager
from modules.data_cleaning import DataCleaner
from modules.statistical_analysis import StatisticalAnalyzer
from modules.visualization import VisualizationEngine

# UX Enhancement: Add progress tracking
def track_user_progress():
    """Track which steps user has completed for better guidance"""
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'data_loaded': False,
            'data_cleaned': False,
            'analysis_done': False,
            'visualization_created': False,
            'data_exported': False
        }
    
    # Update progress based on session state
    if st.session_state.data is not None:
        st.session_state.progress['data_loaded'] = True
    if st.session_state.cleaned_data is not None:
        st.session_state.progress['data_cleaned'] = True

def show_progress_indicator():
    """UX Enhancement: Visual progress indicator in sidebar"""
    if 'progress' in st.session_state:
        progress = st.session_state.progress
        completed = sum(progress.values())
        total = len(progress)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Your Progress")
        
        # Progress bar
        progress_pct = completed / total
        st.sidebar.progress(progress_pct)
        st.sidebar.caption(f"{completed}/{total} steps completed")
        
        # Checklist with visual feedback
        steps = [
            ("📁 Data Loaded", progress['data_loaded']),
            ("🧹 Data Cleaned", progress['data_cleaned']),
            ("📊 Analysis Done", progress['analysis_done']),
            ("📈 Chart Created", progress['visualization_created']),
            ("💾 Data Exported", progress['data_exported'])
        ]
        
        for step, done in steps:
            icon = "✅" if done else "⏳"
            st.sidebar.caption(f"{icon} {step}")

def main():
    # Page configuration
    st.set_page_config(
        page_title="DataDash Analytics",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/ThekingGST/DataDash',
            'Report a bug': 'https://github.com/ThekingGST/DataDash/issues',
            'About': '# DataDash Analytics\nA modern data analysis platform'
        }
    )
    
    # Custom CSS - Futuristic Dark Theme with Glassmorphism
    st.markdown("""
        <style>
        /* Import Google Fonts with fallbacks */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Global Styles with font fallback */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif !important;
        }
        
        /* Main Background */
        .stApp {
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        /* Animated Gradient Header */
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 2rem 0 1rem 0;
            animation: gradientShift 8s ease infinite;
            letter-spacing: -0.02em;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        /* Glassmorphic Containers */
        .glass-card {
            background: rgba(26, 26, 46, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(124, 58, 237, 0.4);
            box-shadow: 0 12px 40px 0 rgba(124, 58, 237, 0.3);
        }
        
        /* Enhanced Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(102, 126, 234, 0.05) 100%);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-left: 4px solid #7c3aed;
            box-shadow: 0 4px 16px rgba(124, 58, 237, 0.1);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateX(4px);
            border-left-width: 6px;
            box-shadow: 0 6px 24px rgba(124, 58, 237, 0.2);
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15, 15, 30, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(124, 58, 237, 0.2);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
            color: #e2e8f0;
            font-weight: 700;
            font-size: 1.5rem;
        }
        
        /* Radio Button Navigation with Neon Effect */
        .stRadio > div {
            gap: 0.5rem;
        }
        
        .stRadio > div > label {
            background: rgba(26, 26, 46, 0.4);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stRadio > div > label:hover {
            background: rgba(124, 58, 237, 0.15);
            border-color: rgba(124, 58, 237, 0.4);
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
        }
        
        .stRadio > div > label[data-checked="true"] {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(102, 126, 234, 0.3));
            border-color: #7c3aed;
            box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3), inset 0 0 20px rgba(124, 58, 237, 0.1);
        }
        
        /* Enhanced Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #7c3aed 0%, #667eea 100%);
            color: white;
            border: none;
            border-radius: 0.75rem;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.5);
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Tabs Enhancement */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: rgba(26, 26, 46, 0.4);
            border-radius: 1rem;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 3.5rem;
            padding: 0 2rem;
            background: transparent;
            border-radius: 0.75rem;
            color: #94a3b8;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(124, 58, 237, 0.1);
            color: #e2e8f0;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(102, 126, 234, 0.3));
            color: white;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
        }
        
        /* Data Tables */
        .stDataFrame {
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        
        /* Metrics Enhancement */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #7c3aed, #667eea);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stMultiSelect > div > div {
            background: rgba(26, 26, 46, 0.6) !important;
            border: 1px solid rgba(124, 58, 237, 0.3) !important;
            border-radius: 0.75rem !important;
            color: #e2e8f0 !important;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within,
        .stMultiSelect > div > div:focus-within {
            border-color: #7c3aed !important;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2) !important;
        }
        
        /* Expander Enhancement */
        .streamlit-expanderHeader {
            background: rgba(26, 26, 46, 0.6);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 0.75rem;
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(124, 58, 237, 0.1);
            border-color: rgba(124, 58, 237, 0.4);
        }
        
        /* Alert/Info Boxes */
        .stAlert {
            background: rgba(26, 26, 46, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 0.75rem;
            border-left: 4px solid;
            padding: 1rem 1.5rem;
        }
        
        /* Success Alert - Green Neon */
        [data-baseweb="notification"][kind="success"] {
            border-left-color: #10b981;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
        }
        
        /* Info Alert - Blue Neon */
        [data-baseweb="notification"][kind="info"] {
            border-left-color: #3b82f6;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
        }
        
        /* Warning Alert - Yellow Neon */
        [data-baseweb="notification"][kind="warning"] {
            border-left-color: #f59e0b;
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.2);
        }
        
        /* Error Alert - Red Neon */
        [data-baseweb="notification"][kind="error"] {
            border-left-color: #ef4444;
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #7c3aed, #667eea, #00f2fe);
            border-radius: 1rem;
        }
        
        /* Slider Enhancement */
        .stSlider > div > div > div {
            background: rgba(124, 58, 237, 0.2);
        }
        
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, #7c3aed, #667eea);
        }
        
        /* Loading Animation */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .stSpinner > div {
            border-color: #7c3aed !important;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* Smooth Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(26, 26, 46, 0.4);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #7c3aed, #667eea);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #8b5cf6, #7c3aed);
        }
        
        /* Separator */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.5), transparent);
            margin: 2rem 0;
        }
        
        /* Download Button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(102, 126, 234, 0.2));
            border: 1px solid rgba(124, 58, 237, 0.4);
            color: #e2e8f0;
            border-radius: 0.75rem;
            transition: all 0.3s ease;
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(102, 126, 234, 0.3));
            border-color: #7c3aed;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3);
        }
        
        /* File Uploader */
        [data-testid="stFileUploader"] {
            background: rgba(26, 26, 46, 0.6);
            border: 2px dashed rgba(124, 58, 237, 0.4);
            border-radius: 1rem;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: #7c3aed;
            background: rgba(124, 58, 237, 0.05);
        }
        
        /* Checkbox and Radio */
        .stCheckbox, .stRadio {
            color: #e2e8f0;
        }
        
        /* Add subtle glow to headings */
        h1, h2, h3 {
            color: #e2e8f0;
            text-shadow: 0 0 20px rgba(124, 58, 237, 0.3);
        }
        
        /* Caption text */
        .caption {
            color: #94a3b8;
            font-size: 0.875rem;
        }
        
        /* UX Enhancement: Focus visible for accessibility */
        *:focus-visible {
            outline: 2px solid #7c3aed;
            outline-offset: 2px;
            border-radius: 0.25rem;
        }
        
        /* UX Enhancement: Reduced motion for accessibility */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        /* UX Enhancement: Loading skeleton */
        .skeleton {
            background: linear-gradient(90deg, rgba(26, 26, 46, 0.4) 25%, rgba(124, 58, 237, 0.1) 50%, rgba(26, 26, 46, 0.4) 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* UX Enhancement: Tooltip styling */
        .tooltip {
            background: rgba(15, 15, 30, 0.95);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        /* UX Enhancement: High contrast mode support */
        @media (prefers-contrast: high) {
            .glass-card {
                border: 2px solid #7c3aed;
            }
            
            .stButton > button {
                border: 2px solid white;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header with animated gradient
    st.markdown('<h1 class="main-header">✨ DataDash Analytics</h1>', 
                unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # UX Enhancement: Track user progress
    track_user_progress()
    
    # Sidebar navigation with enhanced styling and UX improvements
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.caption("Choose a module to get started")
        st.markdown("")
        
        # UX: Smart navigation with contextual hints
        nav_options = [
            ("🏠 Home", "Overview and quick start"),
            ("📁 Data Input", "Upload or enter data"),
            ("🧹 Data Cleaning", "Clean and transform" if st.session_state.data is not None else "⚠️ Load data first"),
            ("📊 Analysis", "Statistical insights" if st.session_state.data is not None else "⚠️ Load data first"),
            ("📈 Visualization", "Create charts" if st.session_state.data is not None else "⚠️ Load data first"),
            ("💾 Export", "Download results" if st.session_state.data is not None else "⚠️ Load data first")
        ]
        
        page = st.radio(
            "Select Module",
            [opt[0] for opt in nav_options],
            label_visibility="collapsed",
            help="Navigate between different modules"
        )
        
        st.markdown("---")
        
        # Show data info if loaded with enhanced styling and UX feedback
        if st.session_state.data is not None:
            st.success("✅ **Data Loaded**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📋 Rows", f"{len(st.session_state.data):,}")
            with col2:
                st.metric("📊 Cols", len(st.session_state.data.columns))
            
            if st.session_state.cleaned_data is not None:
                st.info("🧹 **Cleaned Available**")
            
            # UX: Quick actions for loaded data
            with st.expander("⚡ Quick Actions"):
                if st.button("🔄 Reset Data", use_container_width=True, help="Clear all data and start over"):
                    if st.session_state.get('confirm_reset', False):
                        st.session_state.data = None
                        st.session_state.cleaned_data = None
                        # UX: Safely reset progress if it exists
                        if 'progress' in st.session_state:
                            st.session_state.progress = {k: False for k in st.session_state.progress}
                        st.session_state.confirm_reset = False
                        st.rerun()
                    else:
                        st.session_state.confirm_reset = True
                        st.warning("Click again to confirm reset")
                
                if st.session_state.get('confirm_reset', False):
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.confirm_reset = False
                        st.rerun()
        else:
            st.warning("⚠️ No data loaded")
            st.caption("💡 Tip: Start by loading data")
            
            # UX: Onboarding guidance for new users
            with st.expander("🎯 Getting Started Guide"):
                st.markdown("""
                1. **Load Data**: Go to Data Input
                2. **Clean**: Remove duplicates, handle missing values
                3. **Analyze**: Generate statistics
                4. **Visualize**: Create charts
                5. **Export**: Download results
                """)
        
        # UX Enhancement: Show progress indicator
        show_progress_indicator()
        
        st.markdown("---")
        st.caption("💫 Session active")
        
        # UX: Accessibility - Keyboard shortcuts hint (Note: Shortcuts require browser extension or custom implementation)
        with st.expander("⌨️ Keyboard Navigation"):
            st.caption("Use Tab to navigate between elements")
            st.caption("Use Enter/Space to activate buttons")
            st.caption("Use Arrow keys in dropdowns")
            st.caption("Use Esc to close dialogs")
    
    # Route to pages
    if page == "🏠 Home":
        show_home_page()
    elif page == "📁 Data Input":
        show_data_input_page()
    elif page == "🧹 Data Cleaning":
        show_cleaning_page()
    elif page == "📊 Analysis":
        show_analysis_page()
    elif page == "📈 Visualization":
        show_visualization_page()
    elif page == "💾 Export":
        show_export_page()


def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'data': None,
        'cleaned_data': None,
        'analysis_results': {},
        'current_step': 'input',
        'data_source': None,
        'processing_history': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def show_home_page():
    """Landing page with enhanced futuristic design"""
    # Hero section
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
                Welcome to DataDash Analytics 🚀
            </h2>
            <p style="font-size: 1.25rem; color: #94a3b8; max-width: 700px; margin: 0 auto;">
                Transform your data into actionable insights with our powerful, 
                no-code analytics platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Start Guide with glass cards
    st.markdown("### ✨ Quick Start Guide")
    st.markdown("")
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">📁 Step 1: Load Data</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li style="padding: 0.5rem 0;">✓ Upload CSV/Excel files</li>
                <li style="padding: 0.5rem 0;">✓ Manual data entry</li>
                <li style="padding: 0.5rem 0;">✓ Sample datasets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">🧹 Step 2: Clean Data</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li style="padding: 0.5rem 0;">✓ Filter rows & columns</li>
                <li style="padding: 0.5rem 0;">✓ Handle missing values</li>
                <li style="padding: 0.5rem 0;">✓ Transform data types</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">📊 Step 3: Analyze</h3>
            <ul style="list-style: none; padding-left: 0;">
                <li style="padding: 0.5rem 0;">✓ Statistical analysis</li>
                <li style="padding: 0.5rem 0;">✓ Interactive charts</li>
                <li style="padding: 0.5rem 0;">✓ Export results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Show dataset overview if data loaded
    if st.session_state.data is not None:
        st.markdown("### 📊 Current Dataset Overview")
        st.markdown("")
        
        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("📋 Total Rows", f"{len(st.session_state.data):,}")
        with col2:
            st.metric("📊 Columns", len(st.session_state.data.columns))
        with col3:
            st.metric("💾 Memory", f"{st.session_state.data.memory_usage(deep=True).sum() / 1024:.1f} KB")
        with col4:
            st.metric("🔍 Duplicates", st.session_state.data.duplicated().sum())
        with col5:
            missing_pct = (st.session_state.data.isnull().sum().sum() / 
                          (len(st.session_state.data) * len(st.session_state.data.columns)) * 100)
            st.metric("⚠️ Missing", f"{missing_pct:.1f}%")
        
        st.markdown("")
        
        tab1, tab2, tab3 = st.tabs(["📋 Preview", "ℹ️ Info", "📈 Summary"])
        
        with tab1:
            st.dataframe(st.session_state.data.head(10), use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Data Types:**")
                dtype_df = pd.DataFrame({
                    'Column': st.session_state.data.dtypes.index,
                    'Type': st.session_state.data.dtypes.values.astype(str)
                })
                st.dataframe(dtype_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**Missing Values:**")
                missing_df = pd.DataFrame({
                    'Column': st.session_state.data.columns,
                    'Missing': st.session_state.data.isnull().sum().values,
                    'Percentage': (st.session_state.data.isnull().sum().values / 
                                 len(st.session_state.data) * 100).round(2)
                })
                st.dataframe(missing_df, use_container_width=True, hide_index=True)
        
        with tab3:
            st.dataframe(st.session_state.data.describe(), use_container_width=True)
    else:
        # Empty state with engaging design
        st.markdown("""
            <div style="text-align: center; padding: 3rem 2rem; 
                        background: rgba(26, 26, 46, 0.4); 
                        border-radius: 1rem; 
                        border: 2px dashed rgba(124, 58, 237, 0.3);">
                <h3 style="font-size: 2rem; margin-bottom: 1rem;">🎯 Ready to Start?</h3>
                <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;">
                    Load your data to unlock powerful analytics capabilities
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sample data options with improved layout
        st.markdown("### 📦 Try with Sample Data")
        st.markdown("")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📊 Sales Dataset", use_container_width=True):
                sample_data = pd.DataFrame({
                    'Date': pd.date_range('2024-01-01', periods=100),
                    'Product': np.random.choice(['A', 'B', 'C', 'D'], 100),
                    'Sales': np.random.randint(100, 1000, 100),
                    'Revenue': np.random.randint(1000, 10000, 100),
                    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
                })
                st.session_state.data = sample_data
                st.session_state.data_source = 'sample'
                st.rerun()
        
        with col2:
            if st.button("🌸 Iris Dataset", use_container_width=True):
                try:
                    from sklearn.datasets import load_iris
                    iris = load_iris()
                    sample_data = pd.DataFrame(
                        data=iris.data,
                        columns=iris.feature_names
                    )
                    sample_data['species'] = iris.target
                    st.session_state.data = sample_data
                    st.session_state.data_source = 'sample'
                    st.rerun()
                except ImportError:
                    st.error("❌ scikit-learn not installed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col3:
            if st.button("📈 Random Data", use_container_width=True):
                sample_data = pd.DataFrame({
                    'ID': range(1, 51),
                    'Value_A': np.random.randn(50),
                    'Value_B': np.random.randn(50) * 10,
                    'Category': np.random.choice(['X', 'Y', 'Z'], 50)
                })
                st.session_state.data = sample_data
                st.session_state.data_source = 'sample'
                st.rerun()


def show_data_input_page():
    """Data input page with enhanced UX and accessibility"""
    # UX: Clear page title and description
    st.markdown("## 📁 Data Input")
    st.caption("Upload your dataset or create one manually")
    st.markdown("")
    
    # UX: Progressive disclosure - show method selection first
    input_method = st.radio(
        "Choose how you want to add data:",
        ["📤 Upload File", "✏️ Manual Entry", "📦 Sample Data"],
        horizontal=True,
        help="Select the method that works best for you"
    )
    
    st.markdown("")
    
    if input_method == "📤 Upload File":
        # UX: Contextual help
        with st.expander("💡 Upload Tips", expanded=False):
            st.markdown("""
            - **Supported formats**: CSV, Excel (.xlsx, .xls), JSON
            - **Max file size**: 200 MB
            - **Best practice**: Ensure first row contains column names
            """)
        
        df = DataInputManager.file_uploader()
        if df is not None:
            st.session_state.data = df
            st.session_state.data_source = 'upload'
            st.session_state.progress['data_loaded'] = True
            st.balloons()
            st.success("✅ Data loaded successfully!")
            
            # UX: Immediate next step suggestion
            st.info("💡 **Next Step**: Go to Data Cleaning to prepare your data")
    
    elif input_method == "✏️ Manual Entry":
        # UX: Contextual help
        with st.expander("💡 Manual Entry Tips", expanded=False):
            st.markdown("""
            - **Quick start**: Define columns and rows below
            - **Editable**: Click any cell to edit
            - **Dynamic**: Add/remove rows as needed
            """)
        
        df = DataInputManager.manual_entry()
        if df is not None:
            st.session_state.data = df
            st.session_state.data_source = 'manual'
            st.session_state.progress['data_loaded'] = True
            
            # UX: Immediate next step suggestion
            st.info("💡 **Next Step**: Review your data or proceed to Analysis")
    
    else:  # Sample Data
        st.markdown("### 📦 Load Sample Dataset")
        st.caption("Try the platform with pre-loaded datasets")
        st.markdown("")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="glass-card" style="min-height: 200px;">
                <h4>📊 Sales Data</h4>
                <p style="color: #94a3b8; font-size: 0.9rem;">
                    100 rows of sales transactions with dates, products, and revenue
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Load Sales Data", use_container_width=True, key="load_sales"):
                sample_data = pd.DataFrame({
                    'Date': pd.date_range('2024-01-01', periods=100),
                    'Product': np.random.choice(['Widget A', 'Widget B', 'Widget C', 'Widget D'], 100),
                    'Sales': np.random.randint(100, 1000, 100),
                    'Revenue': np.random.randint(1000, 10000, 100),
                    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
                })
                st.session_state.data = sample_data
                st.session_state.data_source = 'sample'
                st.session_state.progress['data_loaded'] = True
                st.rerun()
        
        with col2:
            st.markdown("""
            <div class="glass-card" style="min-height: 200px;">
                <h4>🌸 Iris Dataset</h4>
                <p style="color: #94a3b8; font-size: 0.9rem;">
                    Classic ML dataset with flower measurements and species classification
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Load Iris Data", use_container_width=True, key="load_iris"):
                try:
                    from sklearn.datasets import load_iris
                    iris = load_iris()
                    sample_data = pd.DataFrame(
                        data=iris.data,
                        columns=iris.feature_names
                    )
                    sample_data['species'] = iris.target
                    st.session_state.data = sample_data
                    st.session_state.data_source = 'sample'
                    st.session_state.progress['data_loaded'] = True
                    st.rerun()
                except ImportError:
                    st.error("❌ scikit-learn not installed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col3:
            st.markdown("""
            <div class="glass-card" style="min-height: 200px;">
                <h4>📈 Random Data</h4>
                <p style="color: #94a3b8; font-size: 0.9rem;">
                    50 rows of synthetic numerical and categorical data for testing
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Load Random Data", use_container_width=True, key="load_random"):
                sample_data = pd.DataFrame({
                    'ID': range(1, 51),
                    'Value_A': np.random.randn(50),
                    'Value_B': np.random.randn(50) * 10,
                    'Category': np.random.choice(['X', 'Y', 'Z'], 50)
                })
                st.session_state.data = sample_data
                st.session_state.data_source = 'sample'
                st.session_state.progress['data_loaded'] = True
                st.rerun()
    
    # Preview section (only show if data exists)
    if st.session_state.data is not None:
        st.markdown("---")
        st.markdown("### 📋 Data Preview")
        st.markdown("")
        
        # UX: Enhanced metrics display
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("📋 Total Rows", f"{len(st.session_state.data):,}")
        with col2:
            st.metric("📊 Columns", len(st.session_state.data.columns))
        with col3:
            st.metric("💾 Memory", f"{st.session_state.data.memory_usage(deep=True).sum() / 1024:.1f} KB")
        with col4:
            st.metric("🔍 Duplicates", st.session_state.data.duplicated().sum())
        with col5:
            st.metric("⚠️ Missing", st.session_state.data.isnull().sum().sum())
        
        st.markdown("")
        
        # UX: Collapsible preview controls
        col1, col2 = st.columns([3, 1])
        
        with col1:
            rows_to_show = st.slider("Rows to display", 5, 50, 10, key="preview_rows",
                                     help="Adjust to see more or fewer rows")
        
        with col2:
            show_index = st.checkbox("Show Index", value=True, key="show_index_data_input",
                                     help="Toggle row index visibility")
        
        # Display dataframe
        if show_index:
            st.dataframe(st.session_state.data.head(rows_to_show), use_container_width=True)
        else:
            st.dataframe(st.session_state.data.head(rows_to_show).reset_index(drop=True), 
                        use_container_width=True)


def show_cleaning_page():
    """Data cleaning page with enhanced UX"""
    # UX: Guard clause with helpful guidance
    if st.session_state.data is None:
        st.warning("⚠️ No data loaded yet")
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3>🔍 Ready to Clean Data?</h3>
            <p style="color: #94a3b8; margin: 1rem 0;">
                First, you need to load some data to clean
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("📁 Go to Data Input", type="primary", use_container_width=True):
            st.session_state.current_step = 'input'
            st.rerun()
        return
    
    st.markdown("## 🧹 Data Cleaning & Transformation")
    st.caption("Prepare your data for analysis")
    st.markdown("")
    
    # UX: Show before state metrics
    with st.expander("📊 Current Data Quality", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", f"{len(st.session_state.data):,}")
        with col2:
            missing = st.session_state.data.isnull().sum().sum()
            st.metric("Missing Values", missing, 
                     delta=f"-{missing}" if missing > 0 else "None",
                     delta_color="inverse")
        with col3:
            dupes = st.session_state.data.duplicated().sum()
            st.metric("Duplicates", dupes,
                     delta=f"-{dupes}" if dupes > 0 else "None",
                     delta_color="inverse")
        with col4:
            completeness = (1 - missing / (len(st.session_state.data) * len(st.session_state.data.columns))) * 100
            st.metric("Completeness", f"{completeness:.1f}%")
    
    st.markdown("")
    
    cleaner = DataCleaner(st.session_state.data)
    cleaned_df = cleaner.show_cleaning_ui()
    
    st.markdown("---")
    
    # UX: Enhanced action buttons with confirmation
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("💾 Save Cleaned Data", type="primary", use_container_width=True,
                    help="Apply all changes and save cleaned version"):
            st.session_state.cleaned_data = cleaned_df
            st.session_state.data = cleaned_df  # Update main data too
            st.session_state.progress['data_cleaned'] = True
            st.success("✅ Cleaned data saved successfully!")
            st.balloons()
            
            # UX: Show improvement metrics
            st.info("💡 **Next Step**: Head to Analysis to explore your clean data")
    
    with col2:
        if st.button("🔄 Reset Changes", use_container_width=True,
                    help="Discard all cleaning operations"):
            if st.session_state.get('confirm_reset_cleaning', False):
                st.session_state.cleaned_data = None
                st.session_state.confirm_reset_cleaning = False
                st.info("Changes reset to original data")
                st.rerun()
            else:
                st.session_state.confirm_reset_cleaning = True
                st.warning("Click again to confirm")
    
    with col3:
        if st.session_state.get('confirm_reset_cleaning', False):
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.confirm_reset_cleaning = False
                st.rerun()


def show_analysis_page():
    """Statistical analysis page with enhanced UX"""
    data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    # UX: Guard clause with helpful guidance
    if data is None:
        st.warning("⚠️ No data available for analysis")
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3>📊 Ready to Analyze?</h3>
            <p style="color: #94a3b8; margin: 1rem 0;">
                Load your data first to unlock powerful analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("📁 Go to Data Input", type="primary", use_container_width=True):
            st.rerun()
        return
    
    st.markdown("## 📊 Statistical Analysis")
    st.caption("Discover insights in your data")
    st.markdown("")
    
    # UX: Quick data overview
    with st.expander("📋 Dataset Overview", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rows", f"{len(data):,}")
        with col2:
            st.metric("Columns", len(data.columns))
        with col3:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            st.metric("Numeric Columns", len(numeric_cols))
        with col4:
            cat_cols = data.select_dtypes(include=['object', 'category']).columns
            st.metric("Categorical Columns", len(cat_cols))
    
    st.markdown("")
    
    analyzer = StatisticalAnalyzer(data)
    analyzer.show_analysis_ui()
    
    # UX: Mark analysis as complete
    st.session_state.progress['analysis_done'] = True


def show_visualization_page():
    """Visualization page with enhanced UX"""
    data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    # UX: Guard clause with helpful guidance
    if data is None:
        st.warning("⚠️ No data available for visualization")
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3>📈 Ready to Visualize?</h3>
            <p style="color: #94a3b8; margin: 1rem 0;">
                Load your data first to create stunning visualizations
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("📁 Go to Data Input", type="primary", use_container_width=True):
            st.rerun()
        return
    
    st.markdown("## 📈 Data Visualization")
    st.caption("Create beautiful, interactive visualizations")
    st.markdown("")
    
    # UX: Quick chart recommendation
    with st.expander("💡 Chart Selection Guide", expanded=False):
        st.markdown("""
        **Choose the right chart:**
        - **Correlation Heatmap**: See relationships between variables
        - **Distribution Plot**: Understand data spread and patterns
        - **Box Plot**: Identify outliers and quartiles
        - **Scatter Plot**: Explore relationships between two variables
        - **Bar Chart**: Compare categories
        - **Line Plot**: Show trends over time
        """)
    
    st.markdown("")
    
    visualizer = VisualizationEngine(data)
    visualizer.show_visualization_ui()
    
    # UX: Mark visualization as complete
    st.session_state.progress['visualization_created'] = True


def show_export_page():
    """Export & download page with enhanced UX"""
    # UX: Guard clause with helpful guidance
    if st.session_state.data is None:
        st.warning("⚠️ No data to export")
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3>💾 Ready to Export?</h3>
            <p style="color: #94a3b8; margin: 1rem 0;">
                First, load and process your data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("📁 Go to Data Input", type="primary", use_container_width=True):
            st.rerun()
        return
    
    st.markdown("## 💾 Export Data & Results")
    st.caption("Download your processed data and analysis results")
    st.markdown("")
    
    data_to_export = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    # UX: Show what will be exported
    st.info(f"📊 Exporting: **{len(data_to_export):,} rows** × **{len(data_to_export.columns)} columns**")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>📊 Export Data</h3>
            <p style="color: #94a3b8; margin-bottom: 1rem;">
                Download your processed dataset
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # CSV export
        csv = data_to_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"datadash_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Best for compatibility and data portability"
        )
        
        # Excel export
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            data_to_export.to_excel(writer, index=False, sheet_name='Data')
        
        st.download_button(
            label="📥 Download as Excel",
            data=buffer.getvalue(),
            file_name=f"datadash_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True,
            help="Best for Excel users and formatted reports"
        )
        
        # JSON export
        json_str = data_to_export.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name=f"datadash_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
            help="Best for developers and API integration"
        )
        
        # UX: Mark export as complete when button is clicked
        if st.button("✅ Mark Export Complete", use_container_width=True):
            st.session_state.progress['data_exported'] = True
            st.success("Export marked as complete!")
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>📋 Summary Report</h3>
            <p style="color: #94a3b8; margin-bottom: 1rem;">
                Generate comprehensive analysis report
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Generate summary report with better formatting
        report = f"""# DataDash Analytics Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Dataset Information
- **Source:** {st.session_state.get('data_source', 'Unknown')}
- **Total Rows:** {len(data_to_export):,}
- **Total Columns:** {len(data_to_export.columns)}
- **Memory Usage:** {data_to_export.memory_usage(deep=True).sum() / 1024:.2f} KB

## Column Information
{data_to_export.dtypes.to_frame('Type').to_string()}

## Descriptive Statistics
{data_to_export.describe().to_string()}

## Missing Values Analysis
{data_to_export.isnull().sum().to_frame('Missing Count').to_string()}

## Data Quality Metrics
- **Completeness:** {((1 - data_to_export.isnull().sum().sum() / (len(data_to_export) * len(data_to_export.columns))) * 100):.2f}%
- **Duplicate Rows:** {data_to_export.duplicated().sum()}
- **Unique Values per Column:**
{data_to_export.nunique().to_frame('Unique Count').to_string()}

---
Report generated by DataDash Analytics Platform
https://github.com/ThekingGST/DataDash
        """
        
        st.download_button(
            label="📥 Download Report (TXT)",
            data=report,
            file_name=f"datadash_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            help="Plain text format for universal compatibility"
        )
        
        # Markdown export
        st.download_button(
            label="📥 Download Report (MD)",
            data=report,
            file_name=f"datadash_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True,
            help="Markdown format for documentation"
        )
        
        # UX: Preview report
        with st.expander("👁️ Preview Report"):
            st.text(report[:500] + "...")
    
    # UX: Success celebration
    if st.session_state.progress.get('data_exported', False):
        st.markdown("---")
        st.success("🎉 **Congratulations!** You've completed the full data analysis workflow!")
        
        # UX: Encourage next steps
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3>What's Next?</h3>
            <p style="color: #94a3b8;">
                Load new data to start another analysis, or share your insights with your team!
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()