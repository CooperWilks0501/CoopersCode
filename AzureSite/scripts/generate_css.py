# generate_css.py

def generate_css(output_path='public/style.css'):
    css_content = """/* public/style.css */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background-color: #f5f5f5;
  color: #333;
}

header {
  background-color: #0078d4;
  color: white;
  padding: 1rem;
  text-align: center;
}

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(700px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.card {
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

.card2 {
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

h2 {
  margin-bottom: 1rem;
  color: #0078d4;
}

.findings-list {
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

.findings-list ul {
  list-style-type: none;
}

.findings-list li {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.findings-list li:last-child {
  border-bottom: none;
}

.findings-list a {
  color: #0078d4;
  text-decoration: none;
}

.findings-list a:hover {
  text-decoration: underline;
}

.error {
  background-color: #ffdddd;
  color: #ff0000;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 5px;
}

.csv-table th {
  text-align: left;
}
"""
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"CSS written to {output_path}")

if __name__ == "__main__":
    generate_css()
