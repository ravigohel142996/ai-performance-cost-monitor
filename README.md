# 🤖 AI Project Performance & Cost Monitor

A production-quality Streamlit dashboard for monitoring AI system health, cost, and performance metrics in real-time.

## 📋 Overview

This application provides comprehensive monitoring capabilities for AI projects, helping teams track cloud costs, evaluate system performance, and identify potential risks before they become critical issues.

## ✨ Features

### 1. **Cost Monitoring**
- Real-time monthly cloud cost estimation
- Cost breakdown by resource type (API calls, RAM, CPU)
- Formula: `cost = (api_calls × 0.002) + (ram × 15) + (cpu × 0.5)`

### 2. **Performance Scoring**
- Dynamic performance scoring (0-100 scale)
- Based on response time and CPU usage
- Visual gauge chart for easy interpretation

### 3. **Risk Assessment**
- Three-tier risk levels: 🟢 Green / 🟡 Yellow / 🔴 Red
- Automatic threshold-based alerts
- Color-coded status indicators

### 4. **System Health Monitoring**
- Overall health status (Excellent/Good/Fair/Poor)
- Real-time metric tracking
- Performance progress visualization

### 5. **Optimization Insights**
- Actionable recommendations
- Resource-specific tips
- Best practice suggestions

### 6. **Additional Features**
- 📥 Download reports as CSV
- 🔄 Reset button for quick resets
- 🌓 Dark/Light mode toggle
- 📊 Interactive visualizations with Plotly
- 💾 Session state management

## 🛠️ Tech Stack

- **Python 3.7+**
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ravigohel142996/ai-performance-cost-monitor.git
cd ai-performance-cost-monitor
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Dashboard:

1. **Configure Project Details** (in sidebar):
   - Enter your project name
   - Set daily users count
   - Input API calls per day

2. **Set Resource Usage**:
   - RAM Usage (GB)
   - CPU Usage (%)
   - Average Response Time (ms)

3. **Click "📈 Calculate"** to generate:
   - Monthly cost estimate
   - Performance score
   - Risk level assessment
   - Optimization tips
   - Downloadable CSV report

4. **Use Additional Features**:
   - Toggle theme mode with 🌓 button
   - Reset inputs with 🔄 button
   - Download reports with 📥 button

## 📊 Input Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| Project Name | Text | Your AI project identifier | "AI ChatBot v1.0" |
| Daily Users | Number | Active users per day | 1000 |
| API Calls per Day | Number | Total daily API requests | 50000 |
| RAM Usage (GB) | Float | Average RAM consumption | 8.0 |
| CPU Usage (%) | Integer | Average CPU utilization | 65 |
| Avg Response Time (ms) | Integer | Mean API response time | 450 |

## 📈 Output Metrics

- **Monthly Cloud Cost**: Estimated monthly expenditure
- **Performance Score**: 0-100 scale based on efficiency
- **Risk Level**: Green/Yellow/Red classification
- **System Health**: Overall health status
- **Optimization Tips**: Actionable recommendations
- **Cost Breakdown**: Detailed cost analysis by resource

## 🏗️ Project Structure

```
ai-performance-cost-monitor/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore rules
```

## 📝 Code Structure

The application follows a modular design with clear separation of concerns:

- **`calculate_monthly_cost()`** - Cost estimation logic
- **`calculate_performance_score()`** - Performance scoring algorithm
- **`determine_risk_level()`** - Risk assessment logic
- **`get_system_health()`** - Health status determination
- **`get_optimization_tips()`** - Recommendation engine
- **`create_performance_gauge()`** - Visualization generation
- **`create_metrics_dataframe()`** - Data export preparation

## 🎯 Use Cases

- **Development Teams**: Monitor development environment costs and performance
- **DevOps Engineers**: Track resource utilization and optimize infrastructure
- **Product Managers**: Understand cost implications of scaling
- **MLOps Teams**: Monitor ML model serving performance and costs

## 🔒 Security & Privacy

- No data is stored or transmitted externally
- All calculations happen locally
- No authentication required for local use

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ by Ravi Gohel

## 🐛 Known Issues

None at this time. Please report any issues you encounter.

## 🚧 Future Enhancements

- Historical data tracking
- Multi-project comparison
- Email alerts for high-risk situations
- Integration with cloud provider APIs
- Advanced analytics and forecasting
- Team collaboration features

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

---

**Note**: This is a monitoring tool for estimation purposes. Actual cloud costs may vary based on specific provider pricing and usage patterns.
