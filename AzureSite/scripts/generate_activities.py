import pandas as pd
def generate_activities_html():
  # Define file paths

  csv_path = r'C:\Users\CWilk\Desktop\PyhtonProj\data\azure_activities.csv'
  output_html_path = r'C:\Users\CWilk\Desktop\PyhtonProj\public\activities.html'

  # Load the CSV-+*
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
    <style>
      .nav-container {{
        position: absolute;
        top: 1rem;
        left: 1rem;
      }}

      .nav-dropdown {{
        padding: 0.5rem;
        font-size: 1rem;
      }}
    </style>
  </head>
  <body>
    <header>
      <div class="nav-container">
        <select class="nav-dropdown" onchange="location = this.value;">
          <option disabled selected>Navigate to...</option>
          <option value="users.html">Users Page</option>
          <option value="activities.html">Activities Page</option>
          <option value="resources.html">Resources Page</option>
          <option value="services.html">Services Page</option>
          <option value="FrontEnd.html">Security Practices</option>
        </select>
      </div>
      <h1>Azure Security Analysis Dashboard</h1>
    </header>
    
    <main>

        <div class="card">
          <h2>Activity Overview</h2>
          <img src="../data/activity_by_hour.png" alt="Activity by Hour" style="max-width: 100%;">
          <canvas id="activityChart"></canvas>
        </div>

        <div class="card">
          <h2>Azure Activites</h2>
          {html_table}
        </div>
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
