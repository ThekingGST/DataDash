# 📊 Interactive Data Analysis Dashboard

A powerful, modern data analysis dashboard built with **Streamlit**, **Pandas**, **NumPy**, and **Seaborn**.

## 🚀 Features

✅ **Data Input**
- Upload CSV, Excel, JSON files
- Manual data entry with Excel-like interface
- Sample datasets included

✅ **Data Cleaning**
- Filter rows and columns
- Handle missing values
- Type conversion
- Column operations (rename, drop, reorder)

✅ **Statistical Analysis**
- Descriptive statistics
- Correlation analysis
- Distribution analysis
- Custom calculations

✅ **Visualization**
- 12+ chart types
- Customizable styling
- Download plots as PNG
- Interactive controls

✅ **Export**
- CSV, Excel, JSON formats
- Summary reports
- Plot exports

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ThekingGST/streamlit-data-dashboard.git
cd streamlit-data-dashboard
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Run the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Quick Start
1. **Load Data**: Upload a file or use sample data
2. **Clean Data**: Use the cleaning tools to prepare your data
3. **Analyze**: Explore statistical insights
4. **Visualize**: Create beautiful charts
5. **Export**: Download your results

## 📁 Project Structure

```
streamlit-data-dashboard/
│
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
│
├── modules/
│   ├── data_input.py              # File upload & manual entry
│   ├── data_cleaning.py           # Cleaning operations
│   ├── statistical_analysis.py    # Statistical analysis
│   └── visualization.py           # Chart generation
│
├── .streamlit/
│   └── config.toml                # Streamlit configuration
│
└── README.md
```

## 🎨 Screenshots

_(Add screenshots of your app here)_

## 🛠️ Technologies Used

- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Seaborn** - Statistical visualization
- **Matplotlib** - Plotting library
- **SciPy** - Scientific computing

## 📝 Requirements

- Python 3.8+
- See `requirements.txt` for package versions

## 🚀 Deployment

### Streamlit Cloud (Free)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Docker
```bash
docker build -t data-dashboard .
docker run -p 8501:8501 data-dashboard
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**ThekingGST**
- GitHub: [@ThekingGST](https://github.com/ThekingGST)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Seaborn for beautiful visualizations
- All open-source contributors

---

Made with ❤️ by ThekingGST