import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

class StatisticalAnalyzer:
    """NumPy-powered statistical analysis"""
    
    def __init__(self, df):
        self.df = df
        self.numeric_df = df.select_dtypes(include=[np.number])
        self.categorical_df = df.select_dtypes(include=['object', 'category'])
    
    def show_analysis_ui(self):
        """Display analysis interface"""
        
        if len(self.numeric_df.columns) == 0:
            st.warning("⚠️ No numeric columns found for analysis!")
            return
        
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["📊 Descriptive Statistics", "🔗 Correlation Analysis", 
             "📈 Distribution Analysis", "🧮 Custom Calculations"],
            key="analysis_type"
        )
        
        st.markdown("---")
        
        if analysis_type == "📊 Descriptive Statistics":
            self.descriptive_stats()
        elif analysis_type == "🔗 Correlation Analysis":
            self.correlation_analysis()
        elif analysis_type == "📈 Distribution Analysis":
            self.distribution_analysis()
        elif analysis_type == "🧮 Custom Calculations":
            self.custom_calculations()
    
    def descriptive_stats(self):
        """Comprehensive descriptive statistics"""
        st.subheader("📊 Descriptive Statistics")
        
        tab1, tab2, tab3 = st.tabs(["📋 Summary Stats", "📊 Detailed View", "🎯 Custom Metrics"])
        
        with tab1:
            st.write("#### Complete Statistical Summary")
            
            # Enhanced describe
            stats_df = self.numeric_df.describe().T
            stats_df['variance'] = self.numeric_df.var()
            stats_df['skewness'] = self.numeric_df.skew()
            stats_df['kurtosis'] = self.numeric_df.kurtosis()
            stats_df['range'] = self.numeric_df.max() - self.numeric_df.min()
            stats_df['cv'] = (self.numeric_df.std() / self.numeric_df.mean() * 100).round(2)
            
            # Reorder columns
            column_order = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 
                          'variance', 'range', 'skewness', 'kurtosis', 'cv']
            stats_df = stats_df[[col for col in column_order if col in stats_df.columns]]
            
            st.dataframe(stats_df.style.background_gradient(cmap='YlOrRd', axis=1), 
                        use_container_width=True)
            
            # Download option
            csv = stats_df.to_csv().encode('utf-8')
            st.download_button(
                label="📥 Download Statistics",
                data=csv,
                file_name="descriptive_statistics.csv",
                mime="text/csv"
            )
        
        with tab2:
            st.write("#### Detailed Column Analysis")
            
            selected_col = st.selectbox("Select column for detailed view", 
                                       self.numeric_df.columns,
                                       key="detailed_col")
            
            data = self.numeric_df[selected_col].dropna()
            
            # Create metrics grid
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Mean", f"{np.mean(data):.4f}")
                st.metric("📊 Median", f"{np.median(data):.4f}")
            
            with col2:
                mode_val = stats.mode(data, keepdims=True)[0][0] if len(data) > 0 else np.nan
                st.metric("📊 Mode", f"{mode_val:.4f}")
                st.metric("📊 Std Dev", f"{np.std(data, ddof=1):.4f}")
            
            with col3:
                st.metric("📊 Variance", f"{np.var(data, ddof=1):.4f}")
                st.metric("📊 Range", f"{np.ptp(data):.4f}")
            
            with col4:
                iqr = np.percentile(data, 75) - np.percentile(data, 25)
                st.metric("📊 IQR", f"{iqr:.4f}")
                cv = (np.std(data, ddof=1) / np.mean(data)) * 100 if np.mean(data) != 0 else 0
                st.metric("📊 CV %", f"{cv:.2f}%")
            
            st.markdown("---")
            
            # Percentiles
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Percentiles:**")
                percentiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
                percentile_values = [np.percentile(data, p*100) for p in percentiles]
                
                percentile_df = pd.DataFrame({
                    'Percentile': [f"{int(p*100)}%" for p in percentiles],
                    'Value': [f"{v:.4f}" for v in percentile_values]
                })
                st.dataframe(percentile_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.write("**Distribution Moments:**")
                moments_df = pd.DataFrame({
                    'Metric': ['Skewness', 'Kurtosis', 'Excess Kurtosis'],
                    'Value': [
                        f"{stats.skew(data):.4f}",
                        f"{stats.kurtosis(data, fisher=False):.4f}",
                        f"{stats.kurtosis(data):.4f}"
                    ],
                    'Interpretation': [
                        '< 0: Left-skewed, > 0: Right-skewed',
                        '3: Normal, > 3: Heavy-tailed',
                        '0: Normal, > 0: Heavy-tailed'
                    ]
                })
                st.dataframe(moments_df, use_container_width=True, hide_index=True)
            
            # Outlier detection
            st.markdown("---")
            st.write("**📍 Outlier Detection (IQR Method):**")
            
            Q1 = np.percentile(data, 25)
            Q3 = np.percentile(data, 75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Lower Bound", f"{lower_bound:.4f}")
            col2.metric("Upper Bound", f"{upper_bound:.4f}")
            col3.metric("Outliers Found", len(outliers))
            
            if len(outliers) > 0:
                st.warning(f"⚠️ Found {len(outliers)} outlier(s) ({len(outliers)/len(data)*100:.2f}% of data)")
        
        with tab3:
            st.write("#### Custom Statistical Metrics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_cols = st.multiselect(
                    "Select columns to compare",
                    self.numeric_df.columns.tolist(),
                    default=self.numeric_df.columns[:min(3, len(self.numeric_df.columns))].tolist(),
                    key="compare_cols"
                )
            
            with col2:
                metric = st.selectbox(
                    "Select metric",
                    ["Mean", "Median", "Std Dev", "Variance", "Min", "Max", "Range"],
                    key="custom_metric"
                )
            
            if selected_cols:
                # Calculate selected metric
                results = {}
                for col in selected_cols:
                    data = self.numeric_df[col].dropna()
                    if metric == "Mean":
                        results[col] = np.mean(data)
                    elif metric == "Median":
                        results[col] = np.median(data)
                    elif metric == "Std Dev":
                        results[col] = np.std(data, ddof=1)
                    elif metric == "Variance":
                        results[col] = np.var(data, ddof=1)
                    elif metric == "Min":
                        results[col] = np.min(data)
                    elif metric == "Max":
                        results[col] = np.max(data)
                    elif metric == "Range":
                        results[col] = np.ptp(data)
                
                # Display as bar chart
                import matplotlib.pyplot as plt
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(results.keys(), results.values(), color='#667eea')
                ax.set_xlabel('Columns', fontsize=12)
                ax.set_ylabel(metric, fontsize=12)
                ax.set_title(f'{metric} Comparison', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                st.pyplot(fig)
                
                # Display table
                result_df = pd.DataFrame({
                    'Column': list(results.keys()),
                    metric: [f"{v:.4f}" for v in results.values()]
                })
                st.dataframe(result_df, use_container_width=True, hide_index=True)
    
    def correlation_analysis(self):
        """Correlation and covariance analysis"""
        st.subheader("🔗 Correlation Analysis")
        
        if len(self.numeric_df.columns) < 2:
            st.warning("⚠️ Need at least 2 numeric columns for correlation analysis")
            return
        
        tab1, tab2 = st.tabs(["📊 Correlation Matrix", "🎯 Pairwise Correlation"])
        
        with tab1:
            st.write("#### Correlation Matrix")
            
            col1, col2 = st.columns(2)
            
            with col1:
                method = st.selectbox("Correlation method", 
                                     ["pearson", "spearman", "kendall"],
                                     key="corr_method")
            
            with col2:
                show_annot = st.checkbox("Show values", value=True, key="corr_annot")
            
            # Calculate correlation
            corr_matrix = self.numeric_df.corr(method=method)
            
            # Display as styled dataframe
            st.dataframe(
                corr_matrix.style.background_gradient(cmap='coolwarm', axis=None, vmin=-1, vmax=1)
                .format("{:.3f}"),
                use_container_width=True
            )
            
            # Visualize with heatmap
            st.write("**Correlation Heatmap:**")
            import seaborn as sns
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=show_annot, fmt=".2f", cmap='coolwarm', 
                       square=True, linewidths=0.5, ax=ax, center=0,
                       vmin=-1, vmax=1, cbar_kws={"shrink": 0.8})
            
            plt.title(f'{method.capitalize()} Correlation Heatmap', fontsize=16, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Strong correlations
            st.markdown("---")
            st.write("**🎯 Strong Correlations (|r| > 0.7):**")
            
            # Find strong correlations
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        strong_corr.append({
                            'Variable 1': corr_matrix.columns[i],
                            'Variable 2': corr_matrix.columns[j],
                            'Correlation': corr_matrix.iloc[i, j],
                            'Strength': 'Strong Positive' if corr_matrix.iloc[i, j] > 0 else 'Strong Negative'
                        })
            
            if strong_corr:
                strong_corr_df = pd.DataFrame(strong_corr)
                st.dataframe(strong_corr_df.style.background_gradient(subset=['Correlation'], 
                            cmap='coolwarm', vmin=-1, vmax=1),
                            use_container_width=True, hide_index=True)
            else:
                st.info("No strong correlations found (threshold: |r| > 0.7)")
            
            # Covariance matrix
            if st.checkbox("Show Covariance Matrix", key="show_cov"):
                st.write("**Covariance Matrix:**")
                cov_matrix = self.numeric_df.cov()
                st.dataframe(
                    cov_matrix.style.background_gradient(cmap='viridis', axis=None)
                    .format("{:.4f}"),
                    use_container_width=True
                )
        
        with tab2:
            st.write("#### Pairwise Correlation Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                var1 = st.selectbox("Select first variable", 
                                   self.numeric_df.columns,
                                   key="var1")
            
            with col2:
                var2 = st.selectbox("Select second variable", 
                                   [c for c in self.numeric_df.columns if c != var1],
                                   key="var2")
            
            if var1 and var2:
                data1 = self.numeric_df[var1].dropna()
                data2 = self.numeric_df[var2].dropna()
                
                # Calculate all correlation methods
                pearson_r, pearson_p = stats.pearsonr(data1, data2)
                spearman_r, spearman_p = stats.spearmanr(data1, data2)
                kendall_r, kendall_p = stats.kendalltau(data1, data2)
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Pearson r", f"{pearson_r:.4f}")
                    st.caption(f"p-value: {pearson_p:.4f}")
                
                with col2:
                    st.metric("Spearman ρ", f"{spearman_r:.4f}")
                    st.caption(f"p-value: {spearman_p:.4f}")
                
                with col3:
                    st.metric("Kendall τ", f"{kendall_r:.4f}")
                    st.caption(f"p-value: {kendall_p:.4f}")
                
                # Scatter plot
                st.write("**Scatter Plot with Regression Line:**")
                import matplotlib.pyplot as plt
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.scatter(data1, data2, alpha=0.6, s=50, color='#667eea')
                
                # Add regression line
                z = np.polyfit(data1, data2, 1)
                p = np.poly1d(z)
                ax.plot(data1, p(data1), "r--", alpha=0.8, linewidth=2, 
                       label=f'y={z[0]:.2f}x+{z[1]:.2f}')
                
                ax.set_xlabel(var1, fontsize=12)
                ax.set_ylabel(var2, fontsize=12)
                ax.set_title(f'{var1} vs {var2} (r={pearson_r:.3f})', 
                           fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                
                st.pyplot(fig)
    
    def distribution_analysis(self):
        """Analyze data distributions"""
        st.subheader("📈 Distribution Analysis")
        
        selected_col = st.selectbox("Select column to analyze", 
                                    self.numeric_df.columns,
                                    key="dist_col")
        
        data = self.numeric_df[selected_col].dropna()
        
        # Distribution metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            skew_val = stats.skew(data)
            st.metric("Skewness", f"{skew_val:.4f}")
            if abs(skew_val) < 0.5:
                st.caption("✅ Fairly symmetric")
            elif skew_val > 0:
                st.caption("⚠️ Right-skewed")
            else:
                st.caption("⚠️ Left-skewed")
        
        with col2:
            kurt_val = stats.kurtosis(data)
            st.metric("Kurtosis", f"{kurt_val:.4f}")
            if abs(kurt_val) < 0.5:
                st.caption("✅ Mesokurtic (normal)")
            elif kurt_val > 0:
                st.caption("📊 Leptokurtic (peaked)")
            else:
                st.caption("📊 Platykurtic (flat)")
        
        with col3:
            # Normality test
            _, p_value = stats.normaltest(data)
            st.metric("Normality p-value", f"{p_value:.4f}")
            if p_value > 0.05:
                st.caption("✅ Likely normal")
            else:
                st.caption("⚠️ Not normal")
        
        with col4:
            # Shapiro-Wilk test (for smaller samples)
            if len(data) < 5000:
                _, sw_p_value = stats.shapiro(data)
                st.metric("Shapiro-Wilk p", f"{sw_p_value:.4f}")
                if sw_p_value > 0.05:
                    st.caption("✅ Passes test")
                else:
                    st.caption("⚠️ Fails test")
            else:
                st.metric("Sample Size", f"{len(data):,}")
                st.caption("Too large for SW test")
        
        st.markdown("---")
        
        # Quantile analysis
        tab1, tab2 = st.tabs(["📊 Quantile Analysis", "📈 Distribution Plots"])
        
        with tab1:
            st.write("#### Quantile Analysis")
            
            quantiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
            quantile_values = [np.percentile(data, q*100) for q in quantiles]
            
            quantile_df = pd.DataFrame({
                'Quantile': [f"{int(q*100)}%" for q in quantiles],
                'Value': [f"{v:.4f}" for v in quantile_values]
            })
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.dataframe(quantile_df, use_container_width=True, hide_index=True)
            
            with col2:
                # Box plot
                import matplotlib.pyplot as plt
                
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.boxplot(data, vert=False, patch_artist=True,
                          boxprops=dict(facecolor='#667eea', alpha=0.5),
                          medianprops=dict(color='red', linewidth=2))
                ax.set_xlabel(selected_col, fontsize=12)
                ax.set_title('Box Plot', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
        
        with tab2:
            st.write("#### Distribution Plots")
            
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            
            # Histogram
            axes[0, 0].hist(data, bins=30, color='#667eea', alpha=0.7, edgecolor='black')
            axes[0, 0].set_title('Histogram', fontweight='bold')
            axes[0, 0].set_xlabel(selected_col)
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].grid(True, alpha=0.3)
            
            # KDE plot
            sns.kdeplot(data, ax=axes[0, 1], fill=True, color='#667eea', alpha=0.5)
            axes[0, 1].set_title('Kernel Density Estimate', fontweight='bold')
            axes[0, 1].set_xlabel(selected_col)
            axes[0, 1].grid(True, alpha=0.3)
            
            # Q-Q plot
            stats.probplot(data, dist="norm", plot=axes[1, 0])
            axes[1, 0].set_title('Q-Q Plot (Normal)', fontweight='bold')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Cumulative distribution
            sorted_data = np.sort(data)
            cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            axes[1, 1].plot(sorted_data, cumulative, color='#667eea', linewidth=2)
            axes[1, 1].set_title('Cumulative Distribution', fontweight='bold')
            axes[1, 1].set_xlabel(selected_col)
            axes[1, 1].set_ylabel('Cumulative Probability')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    def custom_calculations(self):
        """Custom formula evaluator"""
        st.subheader("🧮 Custom Calculations")
        
        st.info("💡 **Tip:** Use column names in your formula. Available operations: +, -, *, /, **, sqrt(), abs(), log(), exp()")
        
        # Show available columns
        with st.expander("📋 Available Columns"):
            col_info = pd.DataFrame({
                'Column Name': self.numeric_df.columns,
                'Type': self.numeric_df.dtypes.values.astype(str),
                'Sample Value': [self.numeric_df[col].iloc[0] if len(self.numeric_df) > 0 else 'N/A' 
                                for col in self.numeric_df.columns]
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            formula = st.text_input(
                "Enter formula",
                placeholder="e.g., Column1 * 2 + Column2",
                key="custom_formula"
            )
        
        with col2:
            new_col_name = st.text_input(
                "New column name", 
                "calculated_column",
                key="new_calc_col"
            )
        
        # Example formulas
        with st.expander("📚 Example Formulas"):
            st.code("""
# Basic arithmetic
Column1 + Column2
Column1 * 2 - Column2 / 3

# Power and square root
Column1 ** 2
Column1 ** 0.5

# Logarithm (requires numpy)
np.log(Column1)
np.log10(Column1)

# Absolute value
abs(Column1 - Column2)

# Exponential
np.exp(Column1)

# Combined operations
(Column1 + Column2) / (Column3 + 1)
            """)
        
        if st.button("🚀 Calculate", type="primary", key="calc_button"):
            if formula:
                try:
                    # Safe evaluation using DataFrame.eval()
                    result = self.df.eval(formula)
                    
                    # Create result dataframe
                    result_df = pd.DataFrame({
                        new_col_name: result
                    })
                    
                    st.success(f"✅ Successfully calculated '{new_col_name}'")
                    
                    # Show results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Preview:**")
                        st.dataframe(result_df.head(10), use_container_width=True)
                    
                    with col2:
                        st.write("**Statistics:**")
                        st.dataframe(result_df.describe(), use_container_width=True)
                    
                    # Option to add to main dataframe
                    if st.button(f"➕ Add '{new_col_name}' to Dataset", key="add_calc_col"):
                        st.session_state.data[new_col_name] = result
                        st.success(f"✅ Added '{new_col_name}' to dataset!")
                        st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error in formula: {str(e)}")
                    st.info("💡 **Troubleshooting:**\n- Check column names are correct\n- Ensure operations are valid\n- Use parentheses for complex formulas")
            else:
                st.warning("⚠️ Please enter a formula")