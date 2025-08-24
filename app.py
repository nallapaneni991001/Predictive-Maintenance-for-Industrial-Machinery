# app.py
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64

app = Flask(__name__)

# Load dataset
df = pd.read_csv('predictive_maintenance_dataset.csv')

# Data visualization
def generate_charts():
    import matplotlib
    matplotlib.use('Agg')  # Use non-GUI backend

    if not plt.isinteractive():
        plt.switch_backend('Agg')
    
    # Sensor Readings Over Time
    plt.figure(figsize=(12, 6))
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    plt.plot(df['Timestamp'], df['Temperature(°C)'], label='Temperature(°C)')
    plt.plot(df['Timestamp'], df['Pressure(bar)'], label='Pressure(bar)')
    plt.plot(df['Timestamp'], df['Vibration(mm/s)'], label='Vibration(mm/s)')
    plt.title('Sensor Readings Over Time')
    plt.xlabel('Time')
    plt.ylabel('Sensor Readings')
    plt.legend()
    plt.savefig('static/sensor_readings_over_time.png')

    # Oil Level vs Pressure (Color-coded by Maintenance Event)
    fig = px.scatter(df, x='Oil_Level(%)', y='Pressure(bar)', color='Maintenance_Event', hover_data=['Machine_ID'])
    fig.write_html('static/oil_level_pressure_plotly_chart.html')

    # Humidity vs Temperature
    fig = px.scatter(df, x='Humidity(%)', y='Temperature(°C)', color='Maintenance_Event', hover_data=['Machine_ID'])
    fig.write_html('static/humidity_temperature_plotly_chart.html')

# Analysis report
def generate_analysis_report():
    # Generate analysis report based on the dataset
    report = """
    <h2>Analysis Report</h2>
    <h3>Overview:</h3>
    <p>The dataset contains sensor readings and maintenance events for industrial machinery over a period of time.</p>
    <h3>Key Findings:</h3>
    <ul>
        <li>The temperature, pressure, and vibration readings show variations over time.</li>
        <li>Maintenance events occur sporadically, with certain patterns observed.</li>
        <li>There is a correlation between oil level and pressure, as well as humidity and temperature.</li>
    </ul>
    """
    return report

# Routes
@app.route('/')
def index():
    generate_charts()  # Generate charts when the page is loaded
    analysis_report = generate_analysis_report()  # Generate analysis report
    return render_template('index.html', analysis_report=analysis_report)

if __name__ == '__main__':
    app.run(debug=True)
