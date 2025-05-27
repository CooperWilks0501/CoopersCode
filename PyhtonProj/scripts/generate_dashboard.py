import pandas as pd

# Define file paths
csv_path = r'C:\Users\CWilk\Desktop\PyhtonProj\data\security_practices.csv'
output_html_path = r'C:\Users\CWilk\Desktop\PyhtonProj\public\FrontEnd.html'

# Load the CSV
df = pd.read_csv(csv_path)

# Convert to HTML table (no index, light table class)
html_table = df.to_html(index=False, classes='csv-table', border=0)

# Construct the full HTML
html_content = f"""<!-- public/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Azure Security Dashboard</title>
  <link rel="stylesheet" href="style.css">
  <script src="chart.js"></script>
</head>
<body>
  <header>
    <h1>Azure Security Analysis Dashboard</h1>
  </header>
  
  <main>
    <section class="dashboard-grid">
      <div class="card">
        <h2>Activity Overview</h2>
        <canvas id="activityChart"></canvas>
      </div>
      
      <div class="card">
        <h2>Anomaly Detection</h2>
        <canvas id="anomalyChart"></canvas>
      </div>
      
      <div class="card">
        <h2>Services by Category</h2>
        <canvas id="servicesChart"></canvas>
      </div>
      
      <div class="card">
        <h2>Security Practices</h2>
        {html_table}
      </div>
    </section>
    
    <section class="details-section">
      <h2>Security Findings</h2>
      <div id="securityFindings" class="findings-list"></div>
    </section>
  </main>
  
  <script src="js/dashboard.js"></script>
</body>
</html>
"""

# Write the file
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Dashboard HTML written to {output_html_path}")
