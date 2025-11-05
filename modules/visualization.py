import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import io

class VisualizationEngine:
    """Seaborn-powered visualization generator"""
    
    def __init__(self, df):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def show_visualization_ui(self):
        """Display visualization interface"""
        
        # Plot type selector
        plot_type = st.selectbox(
            "📊 Select Plot Type",
            [
                "🔥 Correlation Heatmap",
                "📊 Distribution Plot (Histogram + KDE)",
                "📦 Box Plot",
                "🎻 Violin Plot",
                "🔗 Pair Plot",
                "⚫ Scatter Plot",
                "📊 Bar Chart",
                "📈 Count Plot",
                "🌊 KDE Plot",
                "🎯 Joint Plot",
                "📉 Line Plot",
                "🥧 Pie Chart"
            ],
            key="plot_type"
        )
        
        st.markdown("---")
        
        # Common settings in expander
        with st.expander("🎨 Plot Customization Settings"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                palette = st.selectbox(
                    "Color Palette",
                    ["deep", "muted", "bright", "pastel", "dark", "colorblind", 
                     "Set2", "Set3", "husl", "rocket", "viridis"],
                    key="palette"
                )
            
            with col2:
                style = st.selectbox(
                    "Plot Style",
                    ["darkgrid", "whitegrid", "dark", "white", "ticks"],
                    key="style"
                )
            
            with col3:
                context = st.selectbox(
                    "Context",
                    ["notebook", "paper", "talk", "poster"],
                    key="context"
                )
            
            col1, col2 = st.columns(2)
            
            with col1:
                figsize_width = st.slider("Figure Width", 6, 20, 12, key="fig_width")
            
            with col2:
                figsize_height = st.slider("Figure Height", 4, 15, 6, key="fig_height")
        
        # Apply settings
        sns.set_style(style)
        sns.set_palette(palette)
        sns.set_context(context)
        
        # Route to specific plot function
        if "Correlation Heatmap" in plot_type:
            self.plot_heatmap((figsize_width, figsize_height))
        elif "Distribution Plot" in plot_type:
            self.plot_distribution((figsize_width, figsize_height))
        elif "Box Plot" in plot_type:
            self.plot_boxplot((figsize_width, figsize_height))
        elif "Violin Plot" in plot_type:
            self.plot_violin((figsize_width, figsize_height))
        elif "Pair Plot" in plot_type:
            self.plot_pairplot()
        elif "Scatter Plot" in plot_type:
            self.plot_scatter((figsize_width, figsize_height))
        elif "Bar Chart" in plot_type:
            self.plot_bar((figsize_width, figsize_height))
        elif "Count Plot" in plot_type:
            self.plot_count((figsize_width, figsize_height))
        elif "KDE Plot" in plot_type:
            self.plot_kde((figsize_width, figsize_height))
        elif "Joint Plot" in plot_type:
            self.plot_joint()
        elif "Line Plot" in plot_type:
            self.plot_line((figsize_width, figsize_height))
        elif "Pie Chart" in plot_type:
            self.plot_pie((figsize_width, figsize_height))
    
    def plot_heatmap(self, figsize):
        """Correlation heatmap"""
        st.subheader("🔥 Correlation Heatmap")
        
        if not self.numeric_cols:
            st.warning("⚠️ No numeric columns available for correlation heatmap")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            annot = st.checkbox("Show values", value=True, key="hm_annot")
        
        with col2:
            cmap = st.selectbox("Color map", 
                               ["coolwarm", "viridis", "RdYlGn", "RdBu", "YlOrRd", "plasma"],
                               key="hm_cmap")
        
        with col3:
            method = st.selectbox("Correlation method",
                                 ["pearson", "spearman", "kendall"],
                                 key="hm_method")
        
        fig, ax = plt.subplots(figsize=figsize)
        corr = self.df[self.numeric_cols].corr(method=method)
        
        sns.heatmap(corr, annot=annot, fmt=".2f", cmap=cmap,
                   square=True, linewidths=0.5, ax=ax,
                   cbar_kws={"shrink": 0.8}, center=0, vmin=-1, vmax=1)
        
        plt.title(f'{method.capitalize()} Correlation Heatmap', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, "correlation_heatmap")
    
    def plot_distribution(self, figsize):
        """Distribution plot (histogram + KDE)"""
        st.subheader("📊 Distribution Plot")
        
        if not self.numeric_cols:
            st.warning("⚠️ No numeric columns available")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            col = st.selectbox("Select column", self.numeric_cols, key="dist_col")
        
        with col2:
            bins = st.slider("Number of bins", 10, 100, 30, key="dist_bins")
        
        with col3:
            show_kde = st.checkbox("Show KDE", value=True, key="dist_kde")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.histplot(data=self.df, x=col, bins=bins, kde=show_kde, ax=ax, alpha=0.7)
        
        # Add mean and median lines
        mean_val = self.df[col].mean()
        median_val = self.df[col].median()
        
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
        
        plt.title(f'Distribution of {col}', fontsize=16, fontweight='bold')
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"distribution_{col}")
    
    def plot_boxplot(self, figsize):
        """Box plot for outlier detection"""
        st.subheader("📦 Box Plot")
        
        if not self.numeric_cols:
            st.warning("⚠️ No numeric columns available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            y_col = st.selectbox("Select Y axis (numeric)", self.numeric_cols, key="box_y")
        
        with col2:
            x_col = None
            if self.categorical_cols:
                use_grouping = st.checkbox("Group by category", key="box_group")
                if use_grouping:
                    x_col = st.selectbox("Select X axis (category)", 
                                        self.categorical_cols, key="box_x")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if x_col:
            sns.boxplot(data=self.df, x=x_col, y=y_col, ax=ax)
            plt.xticks(rotation=45, ha='right')
        else:
            sns.boxplot(data=self.df, y=y_col, ax=ax)
        
        plt.title(f'Box Plot: {y_col}', fontsize=16, fontweight='bold')
        plt.ylabel(y_col, fontsize=12)
        if x_col:
            plt.xlabel(x_col, fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"boxplot_{y_col}")
    
    def plot_violin(self, figsize):
        """Violin plot"""
        st.subheader("🎻 Violin Plot")
        
        if not self.numeric_cols:
            st.warning("⚠️ No numeric columns available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            y_col = st.selectbox("Select Y axis (numeric)", self.numeric_cols, key="violin_y")
        
        with col2:
            x_col = None
            if self.categorical_cols:
                use_grouping = st.checkbox("Group by category", key="violin_group")
                if use_grouping:
                    x_col = st.selectbox("Select X axis (category)", 
                                        self.categorical_cols, key="violin_x")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if x_col:
            sns.violinplot(data=self.df, x=x_col, y=y_col, ax=ax)
            plt.xticks(rotation=45, ha='right')
        else:
            sns.violinplot(data=self.df, y=y_col, ax=ax)
        
        plt.title(f'Violin Plot: {y_col}', fontsize=16, fontweight='bold')
        plt.ylabel(y_col, fontsize=12)
        if x_col:
            plt.xlabel(x_col, fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"violin_{y_col}")
    
    def plot_pairplot(self):
        """Pair plot for multivariate analysis"""
        st.subheader("🔗 Pair Plot")
        
        if len(self.numeric_cols) < 2:
            st.warning("⚠️ Need at least 2 numeric columns")
            return
        
        st.info("⚠️ Pair plots can be slow with many columns. Select a subset for best performance.")
        
        cols_to_plot = st.multiselect(
            "Select columns (recommended: 3-5 columns)",
            self.numeric_cols,
            default=self.numeric_cols[:min(4, len(self.numeric_cols))],
            key="pair_cols"
        )
        
        if len(cols_to_plot) < 2:
            st.warning("⚠️ Select at least 2 columns")
            return
        
        hue_col = None
        if self.categorical_cols:
            use_hue = st.checkbox("Color by category", key="pair_hue")
            if use_hue:
                hue_col = st.selectbox("Select category", self.categorical_cols, key="pair_cat")
        
        diag_kind = st.selectbox("Diagonal plot type", ["kde", "hist"], key="pair_diag")
        
        with st.spinner("Generating pair plot... This may take a moment."):
            try:
                fig = sns.pairplot(
                    self.df[cols_to_plot + ([hue_col] if hue_col else [])],
                    hue=hue_col,
                    diag_kind=diag_kind,
                    corner=False
                )
                
                st.pyplot(fig)
                self._add_download_button(fig.fig, "pairplot")
            
            except Exception as e:
                st.error(f"❌ Error generating pair plot: {str(e)}")
    
    def plot_scatter(self, figsize):
        """Scatter plot"""
        st.subheader("⚫ Scatter Plot")
        
        if len(self.numeric_cols) < 2:
            st.warning("⚠️ Need at least 2 numeric columns")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_col = st.selectbox("X axis", self.numeric_cols, key="scatter_x")
        
        with col2:
            y_col = st.selectbox("Y axis",
                                [c for c in self.numeric_cols if c != x_col],
                                key="scatter_y")
        
        col1, col2, col3 = st.columns(3)
        
        hue_col = None
        size_col = None
        
        with col1:
            if self.categorical_cols:
                use_hue = st.checkbox("Color by category", key="scatter_hue")
                if use_hue:
                    hue_col = st.selectbox("Category", self.categorical_cols, key="scatter_cat")
        
        with col2:
            use_size = st.checkbox("Size by value", key="scatter_size_check")
            if use_size:
                size_col = st.selectbox("Size variable", self.numeric_cols, key="scatter_size")
        
        with col3:
            add_regression = st.checkbox("Add regression line", value=False, key="scatter_reg")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.scatterplot(data=self.df, x=x_col, y=y_col,
                       hue=hue_col, size=size_col, ax=ax, alpha=0.6, s=100)
        
        # Add regression line if requested
        if add_regression:
            sns.regplot(data=self.df, x=x_col, y=y_col, ax=ax,
                       scatter=False, color='red', line_kws={'linewidth': 2})
        
        plt.title(f'{y_col} vs {x_col}', fontsize=16, fontweight='bold')
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"scatter_{x_col}_{y_col}")
    
    def plot_bar(self, figsize):
        """Bar chart"""
        st.subheader("📊 Bar Chart")
        
        if not self.categorical_cols:
            st.warning("⚠️ No categorical columns available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_col = st.selectbox("Category (X axis)", self.categorical_cols, key="bar_x")
        
        with col2:
            if self.numeric_cols:
                y_col = st.selectbox("Value (Y axis)", self.numeric_cols, key="bar_y")
                agg_func = st.selectbox("Aggregation",
                                       ["mean", "sum", "count", "median", "std"],
                                       key="bar_agg")
            else:
                y_col = None
                agg_func = "count"
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if y_col:
            plot_data = self.df.groupby(x_col)[y_col].agg(agg_func).reset_index()
            plot_data = plot_data.sort_values(y_col, ascending=False)
            sns.barplot(data=plot_data, x=x_col, y=y_col, ax=ax)
            plt.ylabel(f'{y_col} ({agg_func})', fontsize=12)
        else:
            value_counts = self.df[x_col].value_counts()
            plot_data = pd.DataFrame({x_col: value_counts.index, 'count': value_counts.values})
            sns.barplot(data=plot_data, x=x_col, y='count', ax=ax)
            plt.ylabel('Count', fontsize=12)
        
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Bar Chart: {x_col}', fontsize=16, fontweight='bold')
        plt.xlabel(x_col, fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"bar_{x_col}")
    
    def plot_count(self, figsize):
        """Count plot for categorical data"""
        st.subheader("📈 Count Plot")
        
        if not self.categorical_cols:
            st.warning("⚠️ No categorical columns available")
            return
        
        col = st.selectbox("Select category", self.categorical_cols, key="count_col")
        
        # Optional hue
        hue_col = None
        if len(self.categorical_cols) > 1:
            use_hue = st.checkbox("Split by another category", key="count_hue")
            if use_hue:
                hue_col = st.selectbox("Select second category",
                                      [c for c in self.categorical_cols if c != col],
                                      key="count_cat")
        
        fig, ax = plt.subplots(figsize=figsize)
        sns.countplot(data=self.df, x=col, hue=hue_col, ax=ax)
        
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Count Plot: {col}', fontsize=16, fontweight='bold')
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"count_{col}")
    
    def plot_kde(self, figsize):
        """KDE plot"""
        st.subheader("🌊 KDE Plot (Kernel Density Estimation)")
        
        if not self.numeric_cols:
            st.warning("⚠️ No numeric columns available")
            return
        
        col = st.selectbox("Select column", self.numeric_cols, key="kde_col")
        
        hue_col = None
        if self.categorical_cols:
            use_hue = st.checkbox("Group by category", key="kde_hue")
            if use_hue:
                hue_col = st.selectbox("Category", self.categorical_cols, key="kde_cat")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if hue_col:
            for category in self.df[hue_col].unique():
                subset = self.df[self.df[hue_col] == category][col].dropna()
                if len(subset) > 0:
                    sns.kdeplot(subset, label=str(category), ax=ax, fill=True, alpha=0.3)
            plt.legend(title=hue_col)
        else:
            sns.kdeplot(data=self.df, x=col, ax=ax, fill=True, alpha=0.5)
        
        plt.title(f'KDE Plot: {col}', fontsize=16, fontweight='bold')
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Density", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"kde_{col}")
    
    def plot_joint(self):
        """Joint plot (scatter + distributions)"""
        st.subheader("🎯 Joint Plot")
        
        if len(self.numeric_cols) < 2:
            st.warning("⚠️ Need at least 2 numeric columns")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_col = st.selectbox("X axis", self.numeric_cols, key="joint_x")
        
        with col2:
            y_col = st.selectbox("Y axis",
                                [c for c in self.numeric_cols if c != x_col],
                                key="joint_y")
        
        kind = st.selectbox("Plot kind", ["scatter", "kde", "hex", "reg"], key="joint_kind")
        
        with st.spinner("Generating joint plot..."):
            try:
                fig = sns.jointplot(data=self.df, x=x_col, y=y_col, kind=kind, height=8)
                
                st.pyplot(fig)
                self._add_download_button(fig.fig, f"joint_{x_col}_{y_col}")
            
            except Exception as e:
                st.error(f"❌ Error generating joint plot: {str(e)}")
    
    def plot_line(self, figsize):
        """Line plot"""
        st.subheader("📉 Line Plot")
        
        if not self.numeric_cols:
            st.warning("⚠️ No numeric columns available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_col = st.selectbox("X axis", self.df.columns, key="line_x")
        
        with col2:
            y_cols = st.multiselect("Y axis (select one or more)",
                                   self.numeric_cols,
                                   default=[self.numeric_cols[0]],
                                   key="line_y")
        
        if not y_cols:
            st.warning("⚠️ Please select at least one Y column")
            return
        
        fig, ax = plt.subplots(figsize=figsize)
        
        for y_col in y_cols:
            ax.plot(self.df[x_col], self.df[y_col], marker='o', label=y_col, linewidth=2)
        
        plt.title('Line Plot', fontsize=16, fontweight='bold')
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, "lineplot")
    
    def plot_pie(self, figsize):
        """Pie chart"""
        st.subheader("🥧 Pie Chart")
        
        if not self.categorical_cols:
            st.warning("⚠️ No categorical columns available")
            return
        
        col = st.selectbox("Select category", self.categorical_cols, key="pie_col")
        
        top_n = st.slider("Show top N categories", 3, 20, 10, key="pie_top")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        value_counts = self.df[col].value_counts().head(top_n)
        
        colors = sns.color_palette("husl", len(value_counts))
        
        wedges, texts, autotexts = ax.pie(
            value_counts.values,
            labels=value_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.title(f'Distribution of {col} (Top {top_n})', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        st.pyplot(fig)
        self._add_download_button(fig, f"pie_{col}")
    
    def _add_download_button(self, fig, filename_prefix):
        """Add download button for plot"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        
        st.download_button(
            label="📥 Download Plot (PNG)",
            data=buf,
            file_name=f"{filename_prefix}.png",
            mime="image/png",
            use_container_width=True
        )