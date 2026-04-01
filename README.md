# SkyCity-Aukland-bars-and-restaurants

🍽️ SkyCity Restaurant & Bar Analytics Dashboard

An interactive Streamlit dashboard for analyzing restaurant performance across multiple sales channels, geographies, cuisines, and business segments. This project focuses on channel optimization, market insights, and data validation to support strategic decision-making.

📊 Project Overview

This dashboard helps analyze:

Order distribution across channels (In-Store, UberEats, DoorDash, Self-Delivery)
Channel share and dependency
Geographic performance trends
Cuisine and segment-based behavior
Market share and growth patterns
Data validation for forecasting readiness
🎯 Objectives
Primary Objectives
Quantify total order volume by channel
Measure channel share distribution
Identify dominant channels by geography
Secondary Objectives
Compare channel mix across cuisines
Assess channel dependency risk
Support strategic channel planning
⚙️ Features
📌 Interactive filters (Subregion, Cuisine, Segment, Channel type)
📈 KPI metrics (Revenue, Orders, Profit, Margin, AOV)
📦 Channel analysis with share and dependency insights
🌍 Geographic analysis with regional comparisons
🍜 Cuisine & segment-based performance breakdown
🔬 Data validation and variability analysis
📊 Market share and growth distribution
📂 Dataset

The dataset includes:

Order counts by channel
Revenue and profit by channel
Channel share percentages
Subregion, cuisine type, and segment
Growth factor

⚠️ Ensure the file Skycity restaurants & bars.csv is placed in the same directory as the app.

🚀 Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/skycity-dashboard.git
cd skycity-dashboard
2. Install dependencies
pip install -r requirements.txt
3. Run the app
streamlit run app.py
📊 Dashboard Sections
📦 Channel Analysis
Total orders by channel
Channel share distribution
Dependency classification

👉 Insight: Identifies dominant channels and risk of over-dependence

🌍 Geographic Analysis
Orders by subregion
Channel share comparison
Profit by region

👉 Insight: Reveals regional customer behavior and profitability

🍜 Cuisine & Segment Analysis
Channel mix by cuisine
UberEats share by cuisine
Orders by segment

👉 Insight: Highlights which cuisines and segments drive demand

🔬 Forecasting & Validation
Share validation checks
Standard deviation analysis
Market share and growth trends

👉 Insight: Ensures data reliability and supports forecasting

🧠 Key Insights
Balanced channel distribution improves business stability
High dependency on one channel increases risk
Delivery channels drive volume but may reduce margins
Customer behavior varies significantly by region and cuisine
Data validation is critical for accurate forecasting
🛠️ Tech Stack
Python
Streamlit
Pandas
Plotly
📌 Future Improvements
Add time-series forecasting models
Implement anomaly detection
Introduce profit optimization recommendations
Deploy dashboard to cloud (Streamlit Cloud / AWS)
📄 License

This project is open-source and available under the MIT License.

🙌 Acknowledgment

Built for learning and showcasing data analytics, visualization, and business insights using real-world restaurant scenarios.
