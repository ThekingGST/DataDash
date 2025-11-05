import streamlit as st
import pandas as pd
import numpy as np
import io
from modules.data_input import DataInputManager
from modules.data_cleaning import DataCleaner
from modules.statistical_analysis import StatisticalAnalyzer
from modules.visualization import VisualizationEngine

def main():
    # Page configuration
    st.set_page_config(
        page_title="Data Analysis Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 1rem 0;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 24px;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #667eea;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📊 Interactive Data Analysis Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🧭 Navigation")
        st.markdown("---")
        
        page = st.radio(
            "Select Module",
            ["🏠 Home", "📁 Data Input", "🧹 Data Cleaning", 
             "📊 Analysis", "📈 Visualization", "💾 Export"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Show data info if loaded
        if st.session_state.data is not None:
            st.success("✅ **Data Loaded**")
            st.metric("📋 Rows", f"{len(st.session_state.data):,}")
            st.metric("📊 Columns", len(st.session_state.data.columns))
            
            if st.session_state.cleaned_data is not None:
                st.info("🧹 **Cleaned Version Available**")
        else:
            st.warning("⚠️ No data loaded")
        
        st.markdown("---")
        st.caption(f"👤 User: **ThekingGST**")
        st.caption("🕐 Session active")
    
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
    """Landing page with instructions"""
    st.header("Welcome to Your Data Analysis Dashboard! 🎉")
    st.markdown("""
    This interactive dashboard allows you to upload, clean, analyze, and visualize your data 
    with just a few clicks. No coding required!
    """)
    
    st.markdown("### 🚀 Quick Start Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📁 Step 1: Load Data</h3>
            <ul>
                <li>Upload CSV/Excel files</li>
                <li>Or manually enter data</li>
                <li>Preview your dataset</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🧹 Step 2: Clean Data</h3>
            <ul>
                <li>Filter rows & columns</li>
                <li>Handle missing values</li>
                <li>Transform data types</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Step 3: Analyze</h3>
            <ul>
                <li>Statistical analysis</li>
                <li>Interactive charts</li>
                <li>Export results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show dataset overview if data loaded
    if st.session_state.data is not None:
        st.success("### 📋 Current Dataset Overview")
        
        tab1, tab2, tab3 = st.tabs(["📊 Preview", "ℹ️ Info", "📈 Summary"])
        
        with tab1:
            st.dataframe(st.session_state.data.head(10), use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Data Types:**")
                dtype_df = pd.DataFrame({
                    'Column': st.session_state.data.dtypes.index,
                    'Type': st.session_state.data.dtypes.values.astype(str)
                })
                st.dataframe(dtype_df, use_container_width=True)
            
            with col2:
                st.write("**Missing Values:**")
                missing_df = pd.DataFrame({
                    'Column': st.session_state.data.columns,
                    'Missing': st.session_state.data.isnull().sum().values,
                    'Percentage': (st.session_state.data.isnull().sum().values / 
                                 len(st.session_state.data) * 100).round(2)
                })
                st.dataframe(missing_df, use_container_width=True)
        
        with tab3:
            st.dataframe(st.session_state.data.describe(), use_container_width=True)
    else:
        st.info("👈 **Get started by loading your data from the sidebar!**")
        
        # Sample data option
        st.markdown("### 📦 Or Try with Sample Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Load Sample Sales Data"):
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
            if st.button("🌸 Load Iris Dataset"):
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


def show_data_input_page():
    """Data input page with index display"""
    st.header("📁 Data Input")
    st.markdown("Upload your dataset or enter data manually")
    
    input_method = st.radio(
        "Choose input method:",
        ["📤 Upload File", "✏️ Manual Entry"],
        horizontal=True
    )
    
    if input_method == "📤 Upload File":
        df = DataInputManager.file_uploader()
        if df is not None:
            st.session_state.data = df
            st.session_state.data_source = 'upload'
            st.balloons()
            st.success("✅ Data loaded successfully!")
    
    else:  # Manual Entry
        df = DataInputManager.manual_entry()
        if df is not None:
            st.session_state.data = df
            st.session_state.data_source = 'manual'
    
    # Preview
    if st.session_state.data is not None:
        st.markdown("---")
        st.subheader("📋 Data Preview")
        
        # Show row count selector and index toggle
        col1, col2 = st.columns([3, 1])
        
        with col1:
            rows_to_show = st.slider("Rows to display", 5, 50, 10, key="preview_rows")
        
        with col2:
            show_index = st.checkbox("Show Index", value=True, key="show_index_data_input")
        
        # Display dataframe
        if show_index:
            st.dataframe(st.session_state.data.head(rows_to_show), use_container_width=True)
        else:
            st.dataframe(st.session_state.data.head(rows_to_show).reset_index(drop=True), 
                        use_container_width=True)
        
        # Quick stats
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Rows", f"{len(st.session_state.data):,}")
        col2.metric("Total Columns", len(st.session_state.data.columns))
        col3.metric("Memory Usage", f"{st.session_state.data.memory_usage(deep=True).sum() / 1024:.2f} KB")
        col4.metric("Duplicates", st.session_state.data.duplicated().sum())
        col5.metric("Index Type", type(st.session_state.data.index).__name__)


def show_cleaning_page():
    """Data cleaning page"""
    if st.session_state.data is None:
        st.warning("⚠️ Please load data first from the Data Input page!")
        if st.button("Go to Data Input"):
            st.session_state.current_step = 'input'
            st.rerun()
        return
    
    st.header("🧹 Data Cleaning & Transformation")
    st.markdown("Clean and transform your data interactively")
    
    cleaner = DataCleaner(st.session_state.data)
    cleaned_df = cleaner.show_cleaning_ui()
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("💾 Save Cleaned Data", type="primary"):
            st.session_state.cleaned_data = cleaned_df
            st.session_state.data = cleaned_df  # Update main data too
            st.success("✅ Cleaned data saved successfully!")
            st.balloons()
    
    with col2:
        if st.button("🔄 Reset to Original"):
            st.session_state.cleaned_data = None
            st.info("Reset to original data")
            st.rerun()


def show_analysis_page():
    """Statistical analysis page"""
    data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    if data is None:
        st.warning("⚠️ Please load data first!")
        return
    
    st.header("📊 Statistical Analysis")
    st.markdown("Perform comprehensive statistical analysis on your data")
    
    analyzer = StatisticalAnalyzer(data)
    analyzer.show_analysis_ui()


def show_visualization_page():
    """Visualization page"""
    data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    if data is None:
        st.warning("⚠️ Please load data first!")
        return
    
    st.header("📈 Data Visualization")
    st.markdown("Create beautiful, interactive visualizations")
    
    visualizer = VisualizationEngine(data)
    visualizer.show_visualization_ui()


def show_export_page():
    """Export & download page"""
    if st.session_state.data is None:
        st.warning("⚠️ No data to export!")
        return
    
    st.header("💾 Export Data & Results")
    st.markdown("Download your processed data and analysis results")
    
    data_to_export = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Export Data")
        
        # CSV export
        csv = data_to_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="exported_data.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Excel export
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            data_to_export.to_excel(writer, index=False, sheet_name='Data')
        
        st.download_button(
            label="📥 Download as Excel",
            data=buffer.getvalue(),
            file_name="exported_data.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
        
        # JSON export
        json_str = data_to_export.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name="exported_data.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.subheader("📋 Summary Report")
        
        # Generate summary report
        report = f"""
# Data Analysis Summary Report
Generated on: 2025-11-04 15:51:39 UTC
User: ThekingGST

## Dataset Information
- **Source:** {st.session_state.data_source}
- **Total Rows:** {len(data_to_export):,}
- **Total Columns:** {len(data_to_export.columns)}
- **Memory Usage:** {data_to_export.memory_usage(deep=True).sum() / 1024:.2f} KB

## Column Information
{data_to_export.dtypes.to_frame('Type').to_string()}

## Descriptive Statistics
{data_to_export.describe().to_string()}

## Missing Values Analysis
{data_to_export.isnull().sum().to_frame('Missing Count').to_string()}

## Data Quality Score
- Completeness: {((1 - data_to_export.isnull().sum().sum() / (len(data_to_export) * len(data_to_export.columns))) * 100):.2f}%
- Duplicate Rows: {data_to_export.duplicated().sum()}

---
Report generated by Data Analysis Dashboard
        """
        
        st.download_button(
            label="📥 Download Report (TXT)",
            data=report,
            file_name="analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        # Markdown export
        st.download_button(
            label="📥 Download Report (MD)",
            data=report,
            file_name="analysis_report.md",
            mime="text/markdown",
            use_container_width=True
        )


if __name__ == "__main__":
    main()