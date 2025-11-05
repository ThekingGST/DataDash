import streamlit as st
import pandas as pd
import numpy as np

class DataCleaner:
    """Interactive data cleaning operations with enhanced features"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.original_df = df.copy()
    
    def show_cleaning_ui(self):
        """Display cleaning interface with index and column name management"""
        
        # NEW: Index Management Section
        with st.expander("🔢 Index Management"):
            self.index_management()
        
        # Create tabs for different operations
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔍 Filter Data", 
            "🗑️ Handle Missing Values", 
            "🔧 Column Operations",
            "✏️ Rename Columns",  # NEW TAB
            "🔄 Type Conversion"
        ])
        
        with tab1:
            self.filter_interface()
        
        with tab2:
            self.missing_values_interface()
        
        with tab3:
            self.column_operations_interface()
        
        with tab4:
            self.rename_columns_interface()  # NEW FEATURE
        
        with tab5:
            self.type_conversion_interface()
        
        # Show current state with index
        st.markdown("---")
        st.subheader("📊 Current Data State")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            show_index_preview = st.checkbox("Show Index", value=True, key="show_index_preview")
        
        with col1:
            if show_index_preview:
                st.dataframe(self.df.head(10), use_container_width=True)
            else:
                st.dataframe(self.df.head(10).reset_index(drop=True), use_container_width=True)
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", f"{len(self.df):,}")
        col2.metric("Columns", len(self.df.columns))
        col3.metric("Missing", self.df.isnull().sum().sum())
        col4.metric("Index Type", type(self.df.index).__name__)
        
        return self.df
    
    def index_management(self):
        """NEW: Manage DataFrame index"""
        st.markdown("#### 🔢 Index Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Current Index Information:**")
            index_info = pd.DataFrame({
                'Property': ['Index Name', 'Index Type', 'Index Length', 'Has Duplicates'],
                'Value': [
                    str(self.df.index.name) if self.df.index.name else 'None',
                    type(self.df.index).__name__,
                    len(self.df.index),
                    'Yes' if self.df.index.duplicated().any() else 'No'
                ]
            })
            st.dataframe(index_info, use_container_width=True, hide_index=True)
        
        with col2:
            st.write("**Index Operations:**")
            
            index_operation = st.selectbox(
                "Select operation",
                ["Reset Index", "Set Column as Index", "Rename Index", "Drop Index"],
                key="index_operation"
            )
            
            if index_operation == "Reset Index":
                keep_old = st.checkbox("Keep old index as column", value=False, key="keep_old_index")
                if st.button("Reset Index", key="apply_reset_index"):
                    self.df = self.df.reset_index(drop=not keep_old)
                    st.success("✅ Index reset to default (0, 1, 2...)")
            
            elif index_operation == "Set Column as Index":
                if len(self.df.columns) > 0:
                    col_for_index = st.selectbox("Select column", self.df.columns, key="col_for_index")
                    if st.button("Set as Index", key="apply_set_index"):
                        self.df = self.df.set_index(col_for_index)
                        st.success(f"✅ Set '{col_for_index}' as index")
                else:
                    st.warning("No columns available")
            
            elif index_operation == "Rename Index":
                new_index_name = st.text_input("New index name", key="new_index_name")
                if st.button("Rename Index", key="apply_rename_index") and new_index_name:
                    self.df.index.name = new_index_name
                    st.success(f"✅ Index renamed to '{new_index_name}'")
            
            elif index_operation == "Drop Index":
                st.warning("⚠️ This will reset the index to default (0, 1, 2...)")
                if st.button("Drop Index", key="apply_drop_index"):
                    self.df = self.df.reset_index(drop=True)
                    st.success("✅ Index dropped")
        
        # Show index preview
        if st.checkbox("Show index values", value=False, key="show_index_values"):
            st.write("**Index Preview (first 20 values):**")
            st.write(self.df.index[:20].tolist())
    
    def rename_columns_interface(self):
        """NEW: Dedicated interface for renaming columns"""
        st.markdown("#### ✏️ Rename Columns")
        
        rename_method = st.radio(
            "Select rename method:",
            ["Rename Individual Column", "Bulk Rename Columns", "Add Prefix/Suffix", "Clean Column Names"],
            horizontal=False,
            key="rename_method"
        )
        
        if rename_method == "Rename Individual Column":
            st.write("**Rename a Single Column:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                col_to_rename = st.selectbox(
                    "Select column to rename",
                    self.df.columns,
                    key="single_rename_col"
                )
            
            with col2:
                new_name = st.text_input(
                    "New column name",
                    value=col_to_rename,
                    key="single_new_name"
                )
            
            if st.button("Apply Rename", key="apply_single_rename"):
                if new_name and new_name not in self.df.columns:
                    self.df = self.df.rename(columns={col_to_rename: new_name})
                    st.success(f"✅ Renamed '{col_to_rename}' → '{new_name}'")
                elif new_name in self.df.columns:
                    st.error(f"❌ Column '{new_name}' already exists!")
                else:
                    st.error("❌ Please enter a valid name")
        
        elif rename_method == "Bulk Rename Columns":
            st.write("**Rename Multiple Columns at Once:**")
            st.info("💡 Edit the names below and click Apply to rename multiple columns")
            
            # Create editable mapping
            rename_mapping = {}
            
            for i, col in enumerate(self.df.columns):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.text_input("Current", value=col, disabled=True, key=f"bulk_old_{i}")
                
                with col2:
                    new_col_name = st.text_input("New Name", value=col, key=f"bulk_new_{i}")
                    if new_col_name != col:
                        rename_mapping[col] = new_col_name
            
            if st.button("Apply Bulk Rename", key="apply_bulk_rename"):
                if rename_mapping:
                    # Check for duplicates
                    new_names = list(rename_mapping.values())
                    if len(new_names) != len(set(new_names)):
                        st.error("❌ Duplicate column names detected!")
                    else:
                        self.df = self.df.rename(columns=rename_mapping)
                        st.success(f"✅ Renamed {len(rename_mapping)} column(s)")
                else:
                    st.warning("⚠️ No changes detected")
        
        elif rename_method == "Add Prefix/Suffix":
            st.write("**Add Prefix or Suffix to Column Names:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                prefix = st.text_input("Prefix (optional)", key="col_prefix")
            
            with col2:
                suffix = st.text_input("Suffix (optional)", key="col_suffix")
            
            # Select columns to modify
            cols_to_modify = st.multiselect(
                "Select columns to modify (leave empty for all)",
                self.df.columns.tolist(),
                key="prefix_suffix_cols"
            )
            
            if not cols_to_modify:
                cols_to_modify = self.df.columns.tolist()
            
            # Preview
            if prefix or suffix:
                st.write("**Preview:**")
                preview_df = pd.DataFrame({
                    'Original': cols_to_modify,
                    'New Name': [f"{prefix}{col}{suffix}" for col in cols_to_modify]
                })
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
            
            if st.button("Apply Prefix/Suffix", key="apply_prefix_suffix"):
                if prefix or suffix:
                    rename_dict = {col: f"{prefix}{col}{suffix}" for col in cols_to_modify}
                    self.df = self.df.rename(columns=rename_dict)
                    st.success(f"✅ Updated {len(cols_to_modify)} column(s)")
                else:
                    st.warning("⚠️ Please enter a prefix or suffix")
        
        elif rename_method == "Clean Column Names":
            st.write("**Automatically Clean Column Names:**")
            st.info("💡 This will: convert to lowercase, replace spaces with underscores, remove special characters")
            
            cleaning_options = st.multiselect(
                "Select cleaning operations",
                ["Lowercase", "Replace spaces with underscores", "Remove special characters", "Strip whitespace"],
                default=["Lowercase", "Replace spaces with underscores"],
                key="clean_options"
            )
            
            # Preview
            def clean_column_name(col, options):
                cleaned = col
                
                if "Strip whitespace" in options:
                    cleaned = cleaned.strip()
                
                if "Lowercase" in options:
                    cleaned = cleaned.lower()
                
                if "Replace spaces with underscores" in options:
                    cleaned = cleaned.replace(' ', '_')
                
                if "Remove special characters" in options:
                    import re
                    cleaned = re.sub(r'[^a-zA-Z0-9_]', '', cleaned)
                
                return cleaned
            
            if cleaning_options:
                st.write("**Preview:**")
                preview_df = pd.DataFrame({
                    'Original': self.df.columns,
                    'Cleaned': [clean_column_name(col, cleaning_options) for col in self.df.columns]
                })
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
            
            if st.button("Apply Cleaning", key="apply_clean_cols"):
                if cleaning_options:
                    new_columns = [clean_column_name(col, cleaning_options) for col in self.df.columns]
                    self.df.columns = new_columns
                    st.success("✅ Column names cleaned!")
                else:
                    st.warning("⚠️ Please select at least one cleaning option")
        
        # Show current column names
        st.markdown("---")
        st.write("**Current Column Names:**")
        cols_df = pd.DataFrame({
            'Index': range(len(self.df.columns)),
            'Column Name': self.df.columns,
            'Type': self.df.dtypes.values.astype(str)
        })
        st.dataframe(cols_df, use_container_width=True, hide_index=True)
    
    def filter_interface(self):
        """Interactive row/column filtering with string support"""
        st.markdown("#### 🔍 Filter Your Data")
        
        filter_type = st.radio("Filter by:", ["Rows", "Columns"], horizontal=True, key="filter_type_radio")
        
        if filter_type == "Rows":
            st.write("**Filter Rows:**")
            
            # Numeric filtering
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                with st.expander("📊 Filter by Numeric Values"):
                    filter_col = st.selectbox("Select numeric column", numeric_cols, key="filter_num_col")
                    
                    min_val = float(self.df[filter_col].min())
                    max_val = float(self.df[filter_col].max())
                    
                    range_vals = st.slider(
                        f"Select range for {filter_col}",
                        min_val, max_val, (min_val, max_val),
                        key="numeric_range_slider"
                    )
                    
                    if st.button("Apply Numeric Filter", key="apply_num_filter"):
                        before_count = len(self.df)
                        self.df = self.df[
                            (self.df[filter_col] >= range_vals[0]) & 
                            (self.df[filter_col] <= range_vals[1])
                        ]
                        after_count = len(self.df)
                        st.success(f"✅ Filtered: {before_count:,} → {after_count:,} rows ({before_count - after_count:,} removed)")
            
            # NEW: String/Text filtering
            string_cols = self.df.select_dtypes(include=['object', 'string']).columns.tolist()
            
            if string_cols:
                with st.expander("📝 Filter by Text Values"):
                    filter_text_col = st.selectbox("Select text column", string_cols, key="filter_text_col")
                    
                    filter_method = st.selectbox(
                        "Filter method",
                        ["Contains", "Equals", "Starts with", "Ends with", "Does not contain"],
                        key="text_filter_method"
                    )
                    
                    filter_text = st.text_input("Enter text to filter", key="filter_text_input")
                    
                    case_sensitive = st.checkbox("Case sensitive", value=False, key="case_sensitive")
                    
                    if st.button("Apply Text Filter", key="apply_text_filter") and filter_text:
                        before_count = len(self.df)
                        
                        if not case_sensitive:
                            filter_text = filter_text.lower()
                            search_series = self.df[filter_text_col].astype(str).str.lower()
                        else:
                            search_series = self.df[filter_text_col].astype(str)
                        
                        if filter_method == "Contains":
                            mask = search_series.str.contains(filter_text, na=False)
                        elif filter_method == "Equals":
                            mask = search_series == filter_text
                        elif filter_method == "Starts with":
                            mask = search_series.str.startswith(filter_text, na=False)
                        elif filter_method == "Ends with":
                            mask = search_series.str.endswith(filter_text, na=False)
                        elif filter_method == "Does not contain":
                            mask = ~search_series.str.contains(filter_text, na=False)
                        
                        self.df = self.df[mask]
                        after_count = len(self.df)
                        st.success(f"✅ Filtered: {before_count:,} → {after_count:,} rows ({before_count - after_count:,} removed)")
            
            # Remove duplicates
            st.markdown("---")
            st.write("**Remove Duplicate Rows:**")
            duplicates_count = self.df.duplicated().sum()
            st.info(f"Found **{duplicates_count}** duplicate rows")
            
            if duplicates_count > 0:
                subset_cols = st.multiselect(
                    "Check duplicates based on columns (leave empty for all)",
                    self.df.columns.tolist(),
                    key="dup_subset"
                )
                
                if st.button("Remove Duplicates", key="remove_dups"):
                    before = len(self.df)
                    if subset_cols:
                        self.df = self.df.drop_duplicates(subset=subset_cols)
                    else:
                        self.df = self.df.drop_duplicates()
                    after = len(self.df)
                    st.success(f"✅ Removed {before - after} duplicate rows")
        
        else:  # Filter Columns
            st.write("**Select Columns to Keep:**")
            
            selected_cols = st.multiselect(
                "Choose columns",
                self.df.columns.tolist(),
                default=self.df.columns.tolist(),
                key="column_selector_filter"
            )
            
            if st.button("Apply Column Selection", key="apply_col_selection"):
                if len(selected_cols) > 0:
                    removed = len(self.df.columns) - len(selected_cols)
                    self.df = self.df[selected_cols]
                    st.success(f"✅ Kept {len(selected_cols)} columns (removed {removed})")
                else:
                    st.error("❌ Please select at least one column")
    
    def missing_values_interface(self):
        """Handle missing values"""
        st.markdown("#### 🗑️ Handle Missing Values")
        
        # Missing values summary
        missing_summary = pd.DataFrame({
            'Column': self.df.columns,
            'Missing Count': self.df.isnull().sum().values,
            'Missing %': (self.df.isnull().sum().values / len(self.df) * 100).round(2)
        })
        missing_summary = missing_summary[missing_summary['Missing Count'] > 0]
        
        if len(missing_summary) > 0:
            st.dataframe(missing_summary, use_container_width=True, hide_index=True)
            
            strategy = st.selectbox(
                "Select strategy",
                [
                    "Drop rows with any missing values",
                    "Drop rows with all missing values",
                    "Fill numeric with mean",
                    "Fill numeric with median",
                    "Fill numeric with mode",
                    "Fill text with most frequent value",
                    "Fill with forward fill",
                    "Fill with backward fill",
                    "Fill with custom value"
                ],
                key="missing_strategy"
            )
            
            custom_value = None
            if strategy == "Fill with custom value":
                custom_value = st.text_input("Enter custom value", "0", key="custom_fill_value")
            
            if st.button("Apply Missing Value Strategy", key="apply_missing_strategy"):
                try:
                    if strategy == "Drop rows with any missing values":
                        before = len(self.df)
                        self.df = self.df.dropna()
                        st.success(f"✅ Dropped {before - len(self.df)} rows")
                    
                    elif strategy == "Drop rows with all missing values":
                        before = len(self.df)
                        self.df = self.df.dropna(how='all')
                        st.success(f"✅ Dropped {before - len(self.df)} rows")
                    
                    elif strategy == "Fill numeric with mean":
                        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
                        st.success("✅ Filled numeric columns with mean values")
                    
                    elif strategy == "Fill numeric with median":
                        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
                        st.success("✅ Filled numeric columns with median values")
                    
                    elif strategy == "Fill numeric with mode":
                        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                        for col in numeric_cols:
                            mode_val = self.df[col].mode()
                            if len(mode_val) > 0:
                                self.df[col] = self.df[col].fillna(mode_val[0])
                        st.success("✅ Filled numeric columns with mode values")
                    
                    elif strategy == "Fill text with most frequent value":
                        text_cols = self.df.select_dtypes(include=['object', 'string']).columns
                        for col in text_cols:
                            mode_val = self.df[col].mode()
                            if len(mode_val) > 0:
                                self.df[col] = self.df[col].fillna(mode_val[0])
                        st.success("✅ Filled text columns with most frequent values")
                    
                    elif strategy == "Fill with forward fill":
                        self.df = self.df.ffill()
                        st.success("✅ Applied forward fill")
                    
                    elif strategy == "Fill with backward fill":
                        self.df = self.df.bfill()
                        st.success("✅ Applied backward fill")
                    
                    elif strategy == "Fill with custom value":
                        self.df = self.df.fillna(custom_value)
                        st.success(f"✅ Filled with '{custom_value}'")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.success("✅ No missing values found!")
    
    def column_operations_interface(self):
        """Drop and reorder columns"""
        st.markdown("#### 🔧 Column Operations")
        
        operation = st.radio(
            "Select operation",
            ["Drop Columns", "Reorder Columns"],
            horizontal=True,
            key="col_operation"
        )
        
        if operation == "Drop Columns":
            cols_to_drop = st.multiselect(
                "Select columns to drop", 
                self.df.columns,
                key="drop_cols"
            )
            
            if st.button("Drop Selected Columns", key="apply_drop"):
                if len(cols_to_drop) > 0:
                    if len(cols_to_drop) < len(self.df.columns):
                        self.df = self.df.drop(columns=cols_to_drop)
                        st.success(f"✅ Dropped {len(cols_to_drop)} column(s)")
                    else:
                        st.error("❌ Cannot drop all columns!")
                else:
                    st.warning("⚠️ No columns selected")
        
        elif operation == "Reorder Columns":
            st.info("💡 Drag and drop to reorder columns")
            new_order = st.multiselect(
                "Arrange columns in desired order",
                self.df.columns.tolist(),
                default=self.df.columns.tolist(),
                key="reorder_cols"
            )
            
            if st.button("Apply Order", key="apply_reorder"):
                if len(new_order) == len(self.df.columns):
                    self.df = self.df[new_order]
                    st.success("✅ Columns reordered")
                else:
                    st.error("❌ Please include all columns")
    
    def type_conversion_interface(self):
        """Convert column data types with enhanced string support"""
        st.markdown("#### 🔄 Data Type Conversion")
        
        # Current types
        st.write("**Current Data Types:**")
        type_df = pd.DataFrame({
            'Column': self.df.dtypes.index,
            'Current Type': self.df.dtypes.values.astype(str),
            'Non-Null Count': self.df.count().values,
            'Sample Value': [str(self.df[col].iloc[0]) if len(self.df) > 0 else 'N/A' for col in self.df.columns]
        })
        st.dataframe(type_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col_to_convert = st.selectbox("Select column to convert", self.df.columns, key="convert_col")
        
        target_type = st.selectbox(
            "Target type",
            ["String (str)", "Integer (int)", "Float (float)", "DateTime", "Category", "Boolean"],
            key="target_type"
        )
        
        # Show preview
        if col_to_convert:
            st.write(f"**Sample values from '{col_to_convert}':**")
            st.write(self.df[col_to_convert].head().tolist())
        
        if st.button("Convert Type", key="apply_conversion"):
            try:
                if target_type == "String (str)":
                    self.df[col_to_convert] = self.df[col_to_convert].astype(str)
                    st.success(f"✅ Converted '{col_to_convert}' to string")
                
                elif target_type == "Integer (int)":
                    self.df[col_to_convert] = pd.to_numeric(self.df[col_to_convert], errors='coerce').fillna(0).astype('Int64')
                    st.success(f"✅ Converted '{col_to_convert}' to integer")
                    st.info("ℹ️ Non-numeric values were converted to 0")
                
                elif target_type == "Float (float)":
                    self.df[col_to_convert] = pd.to_numeric(self.df[col_to_convert], errors='coerce')
                    st.success(f"✅ Converted '{col_to_convert}' to float")
                    st.info("ℹ️ Non-numeric values were converted to NaN")
                
                elif target_type == "DateTime":
                    self.df[col_to_convert] = pd.to_datetime(self.df[col_to_convert], errors='coerce')
                    st.success(f"✅ Converted '{col_to_convert}' to datetime")
                    st.info("ℹ️ Invalid dates were converted to NaT")
                
                elif target_type == "Category":
                    self.df[col_to_convert] = self.df[col_to_convert].astype('category')
                    st.success(f"✅ Converted '{col_to_convert}' to category")
                    st.info(f"ℹ️ Found {self.df[col_to_convert].nunique()} unique categories")
                
                elif target_type == "Boolean":
                    # Smart boolean conversion
                    self.df[col_to_convert] = self.df[col_to_convert].map({
                        'True': True, 'true': True, '1': True, 1: True, 'yes': True, 'Yes': True,
                        'False': False, 'false': False, '0': False, 0: False, 'no': False, 'No': False
                    })
                    st.success(f"✅ Converted '{col_to_convert}' to boolean")
                    st.info("ℹ️ Recognized: True/False, 1/0, yes/no (case-insensitive)")
            
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")
                st.info("💡 Tip: Check for incompatible values in the column")