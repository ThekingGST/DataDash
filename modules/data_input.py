import streamlit as st
import pandas as pd
import io

class DataInputManager:
    """Handles file upload and manual data entry with enhanced features"""
    
    @staticmethod
    def file_uploader():
        """File upload with validation and enhanced string support"""
        st.markdown("### 📤 Upload Your Dataset")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls', 'json'],
            help="Supported formats: CSV, Excel (.xlsx, .xls), JSON"
        )
        
        if uploaded_file is not None:
            try:
                # Show file info
                file_details = {
                    "Filename": uploaded_file.name,
                    "FileType": uploaded_file.type,
                    "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
                }
                
                with st.expander("📋 File Details"):
                    for key, value in file_details.items():
                        st.write(f"**{key}:** {value}")
                
                # Detect file type and read accordingly
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                with st.spinner("Loading data..."):
                    if file_extension == 'csv':
                        # CSV options
                        with st.expander("⚙️ CSV Import Options"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                delimiter = st.selectbox("Delimiter", [',', ';', '\t', '|'], index=0)
                            
                            with col2:
                                encoding = st.selectbox("Encoding", ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252'], index=0)
                            
                            with col3:
                                # NEW: Option to treat all as strings initially
                                keep_as_string = st.checkbox("Import all as text", value=False,
                                                            help="Prevents automatic type conversion")
                        
                        if keep_as_string:
                            df = pd.read_csv(uploaded_file, delimiter=delimiter, encoding=encoding, dtype=str)
                        else:
                            df = pd.read_csv(uploaded_file, delimiter=delimiter, encoding=encoding)
                    
                    elif file_extension in ['xlsx', 'xls']:
                        # Excel options
                        excel_file = pd.ExcelFile(uploaded_file)
                        sheet_names = excel_file.sheet_names
                        
                        with st.expander("⚙️ Excel Import Options"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if len(sheet_names) > 1:
                                    selected_sheet = st.selectbox("Select sheet", sheet_names)
                                else:
                                    selected_sheet = sheet_names[0]
                                    st.info(f"Using sheet: **{selected_sheet}**")
                            
                            with col2:
                                # NEW: Option to treat all as strings
                                keep_as_string = st.checkbox("Import all as text", value=False,
                                                            help="Prevents automatic type conversion")
                        
                        if keep_as_string:
                            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet, dtype=str)
                        else:
                            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                    
                    elif file_extension == 'json':
                        df = pd.read_json(uploaded_file)
                
                # NEW: Show index information
                st.success(f"✅ Successfully loaded **{len(df):,}** rows and **{len(df.columns)}** columns")
                
                # NEW: Index handling options
                with st.expander("🔢 Index Settings"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        show_index = st.checkbox("Show Index in Preview", value=True, key="show_index_upload")
                        
                    with col2:
                        reset_index = st.checkbox("Reset Index (0, 1, 2...)", value=False, key="reset_index_upload")
                    
                    # Option to set a column as index
                    set_column_as_index = st.checkbox("Set a column as index", value=False, key="set_col_index")
                    
                    if set_column_as_index:
                        index_col = st.selectbox("Select column to use as index", df.columns, key="index_col_select")
                        if st.button("Apply Index", key="apply_index_upload"):
                            df = df.set_index(index_col)
                            st.success(f"✅ Set '{index_col}' as index")
                    
                    if reset_index:
                        df = df.reset_index(drop=True)
                        st.info("Index reset to default (0, 1, 2...)")
                
                # Preview with data type information
                with st.expander("👁️ Preview Data & Types"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("**Data Preview:**")
                        if show_index:
                            st.dataframe(df.head(10), use_container_width=True)
                        else:
                            st.dataframe(df.head(10).reset_index(drop=True), use_container_width=True)
                    
                    with col2:
                        st.write("**Column Types:**")
                        type_df = pd.DataFrame({
                            'Column': df.columns,
                            'Type': df.dtypes.values.astype(str),
                            'Non-Null': df.count().values,
                            'Null': df.isnull().sum().values
                        })
                        st.dataframe(type_df, use_container_width=True, hide_index=True)
                
                return df
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.info("💡 Tip: Make sure your file is properly formatted and not corrupted")
                return None
        
        return None
    
    @staticmethod
    def manual_entry():
        """Enhanced Excel-like manual data entry with string support"""
        st.markdown("### ✏️ Manual Data Entry")
        st.info("💡 Create your dataset from scratch with support for text, numbers, and dates")
        
        # Template configuration
        with st.expander("⚙️ Table Configuration", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                num_cols = st.number_input("Number of columns", min_value=1, max_value=20, value=3, key="manual_num_cols")
            
            with col2:
                num_rows = st.number_input("Number of rows", min_value=1, max_value=100, value=5, key="manual_num_rows")
            
            with col3:
                default_type = st.selectbox(
                    "Default column type",
                    ["Mixed (Auto)", "Text (String)", "Number (Float)", "Integer"],
                    key="manual_default_type"
                )
            
            # NEW: Custom column names
            st.write("**📝 Column Names:**")
            
            if 'manual_column_names' not in st.session_state:
                st.session_state.manual_column_names = [f'Column{i+1}' for i in range(num_cols)]
            
            # Ensure we have the right number of column names
            while len(st.session_state.manual_column_names) < num_cols:
                st.session_state.manual_column_names.append(f'Column{len(st.session_state.manual_column_names)+1}')
            while len(st.session_state.manual_column_names) > num_cols:
                st.session_state.manual_column_names.pop()
            
            # Column name inputs
            col_name_cols = st.columns(min(num_cols, 4))
            for i in range(num_cols):
                with col_name_cols[i % 4]:
                    st.session_state.manual_column_names[i] = st.text_input(
                        f"Col {i+1}",
                        value=st.session_state.manual_column_names[i],
                        key=f"col_name_{i}"
                    )
            
            # NEW: Column type specification
            if st.checkbox("🔧 Specify column types", value=False, key="specify_types"):
                st.write("**Column Types:**")
                
                if 'manual_column_types' not in st.session_state:
                    st.session_state.manual_column_types = ['str'] * num_cols
                
                while len(st.session_state.manual_column_types) < num_cols:
                    st.session_state.manual_column_types.append('str')
                while len(st.session_state.manual_column_types) > num_cols:
                    st.session_state.manual_column_types.pop()
                
                type_cols = st.columns(min(num_cols, 4))
                for i in range(num_cols):
                    with type_cols[i % 4]:
                        st.session_state.manual_column_types[i] = st.selectbox(
                            st.session_state.manual_column_names[i],
                            ['str', 'int', 'float', 'bool'],
                            index=['str', 'int', 'float', 'bool'].index(st.session_state.manual_column_types[i]) if st.session_state.manual_column_types[i] in ['str', 'int', 'float', 'bool'] else 0,
                            key=f"col_type_{i}"
                        )
        
        # Initialize or update template
        if st.button("🔄 Create/Reset Template", key="create_template") or 'manual_data' not in st.session_state:
            # Determine default value based on type
            if default_type == "Text (String)":
                default_val = ""
            elif default_type == "Number (Float)":
                default_val = 0.0
            elif default_type == "Integer":
                default_val = 0
            else:
                default_val = ""
            
            st.session_state.manual_data = pd.DataFrame(
                default_val,
                columns=st.session_state.manual_column_names,
                index=range(num_rows)
            )
            st.success("✅ Template created!")
            st.rerun()
        
        # Update column names if they changed
        if 'manual_data' in st.session_state and list(st.session_state.manual_data.columns) != st.session_state.manual_column_names:
            st.session_state.manual_data.columns = st.session_state.manual_column_names
        
        # Editable table
        st.markdown("#### ✏️ Edit Your Data:")
        st.caption("💡 Tip: Click any cell to edit. Use Tab to move between cells. Add/remove rows using the buttons on the left.")
        
        edited_df = st.data_editor(
            st.session_state.manual_data,
            num_rows="dynamic",  # Allow adding/removing rows
            use_container_width=True,
            key="data_editor",
            column_config={
                col: st.column_config.TextColumn(col) if st.session_state.get('manual_column_types', ['str']*len(st.session_state.manual_data.columns))[i] == 'str'
                else st.column_config.NumberColumn(col, format="%.2f") if st.session_state.get('manual_column_types', ['str']*len(st.session_state.manual_data.columns))[i] == 'float'
                else st.column_config.NumberColumn(col, format="%d") if st.session_state.get('manual_column_types', ['str']*len(st.session_state.manual_data.columns))[i] == 'int'
                else st.column_config.CheckboxColumn(col) if st.session_state.get('manual_column_types', ['str']*len(st.session_state.manual_data.columns))[i] == 'bool'
                else st.column_config.Column(col)
                for i, col in enumerate(st.session_state.manual_data.columns)
            }
        )
        
        # Show current data info
        st.caption(f"📊 Current size: **{len(edited_df)} rows** × **{len(edited_df.columns)} columns**")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Data", type="primary", key="save_manual"):
                # Apply type conversions if specified
                if 'manual_column_types' in st.session_state:
                    for i, col in enumerate(edited_df.columns):
                        try:
                            col_type = st.session_state.manual_column_types[i]
                            if col_type == 'int':
                                edited_df[col] = pd.to_numeric(edited_df[col], errors='coerce').fillna(0).astype(int)
                            elif col_type == 'float':
                                edited_df[col] = pd.to_numeric(edited_df[col], errors='coerce')
                            elif col_type == 'str':
                                edited_df[col] = edited_df[col].astype(str)
                            elif col_type == 'bool':
                                edited_df[col] = edited_df[col].astype(bool)
                        except Exception as e:
                            st.warning(f"⚠️ Could not convert column '{col}' to {col_type}: {str(e)}")
                
                st.session_state.manual_data = edited_df
                st.success("✅ Data saved to session!")
                return edited_df
        
        with col2:
            if st.button("🗑️ Clear All", key="clear_manual"):
                if 'manual_data' in st.session_state:
                    del st.session_state.manual_data
                if 'manual_column_names' in st.session_state:
                    del st.session_state.manual_column_names
                if 'manual_column_types' in st.session_state:
                    del st.session_state.manual_column_types
                st.rerun()
        
        with col3:
            # NEW: Show index option
            show_index_manual = st.checkbox("Show Index", value=True, key="show_index_manual")
        
        # Preview edited data
        if st.checkbox("👁️ Preview Changes", value=False, key="preview_manual"):
            st.write("**Current Data:**")
            if show_index_manual:
                st.dataframe(edited_df, use_container_width=True)
            else:
                st.dataframe(edited_df.reset_index(drop=True), use_container_width=True)
            
            # Show data types
            st.write("**Data Types:**")
            type_info = pd.DataFrame({
                'Column': edited_df.columns,
                'Type': edited_df.dtypes.values.astype(str),
                'Sample': [str(edited_df[col].iloc[0]) if len(edited_df) > 0 else 'N/A' for col in edited_df.columns]
            })
            st.dataframe(type_info, use_container_width=True, hide_index=True)
        
        return None