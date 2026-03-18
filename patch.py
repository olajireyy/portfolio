import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_root = """      :root {
        --primary: #3b82f6;
        --primary-light: #60a5fa;
        --primary-dark: #2563eb;
        --primary-rgb: 59, 130, 246;
        --secondary: #38bdf8;
        --secondary-rgb: 56, 189, 248;
        --accent: #f59e0b;
        --bg-dark: #0f1115;
        --bg-card: #17191e;
        --bg-card-hover: #1f2229;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border: #262a33;
        --gradient-1: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1e40af 100%);
        --gradient-2: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        --shadow-color: rgba(0, 0, 0, 0.5);
        --bg-header: rgba(15, 17, 21, 0.8);
        --bg-header-scrolled: rgba(15, 17, 21, 0.95);
      }

      [data-theme="light"] {
        --primary: #2563eb;
        --primary-light: #3b82f6;
        --primary-dark: #1d4ed8;
        --primary-rgb: 37, 99, 235;
        --secondary: #0284c7;
        --secondary-rgb: 2, 132, 199;
        --accent: #d97706;
        --bg-dark: #fbfbfc;
        --bg-card: #ffffff;
        --bg-card-hover: #f1f5f9;
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --text-muted: #64748b;
        --border: #e2e8f0;
        --gradient-1: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #1e3a8a 100%);
        --gradient-2: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        --shadow-color: rgba(15, 23, 42, 0.1);
        --bg-header: rgba(255, 255, 255, 0.8);
        --bg-header-scrolled: rgba(255, 255, 255, 0.95);
      }"""

# Replace root using regex
html = re.sub(r':root\s*\{[^}]*\}', new_root.strip(), html, count=1)

html = html.replace("rgba(99, 102, 241,", "rgba(var(--primary-rgb),")
html = html.replace("rgba(139, 92, 246,", "rgba(var(--secondary-rgb),")
html = html.replace("rgba(34, 211, 238,", "rgba(var(--secondary-rgb),")

# Replace header CSS
html = re.sub(r'(\.header\s*\{[^}]*?)background:\s*rgba\(10,\s*10,\s*15,\s*0\.8\);', r'\1background: var(--bg-header);', html, flags=re.DOTALL)
html = re.sub(r'(\.header\.scrolled\s*\{[^}]*?)background:\s*rgba\(10,\s*10,\s*15,\s*0\.95\);', r'\1background: var(--bg-header-scrolled);', html, flags=re.DOTALL)
html = re.sub(r'(\.code-preview\s*\{[^}]*?)background:\s*rgba\(10,\s*10,\s*15,\s*0\.95\);', r'\1background: var(--bg-dark);', html, flags=re.DOTALL)
html = re.sub(r'(\.project-overlay\s*\{[^}]*?)background:\s*rgba\(10,\s*10,\s*15,\s*0\.8\);', r'\1background: var(--bg-header);', html, flags=re.DOTALL)
html = re.sub(r'(\.navbar\s*\{[^}]*?)(background:\s*rgba\(10,\s*10,\s*15,\s*0\.98\);)', r'\1background: var(--bg-header-scrolled);', html, flags=re.DOTALL)

# Add theme toggle button
if "id=\"theme-toggle\"" not in html:
    navbar_with_toggle = """        </nav>
        <button id="theme-toggle" aria-label="Toggle Dark Mode" style="background:transparent; border:none; color:var(--text-primary); font-size:2.2rem; cursor:pointer; margin:0 1.5rem; display:flex; align-items:center;">
          <i class='bx bx-sun'></i>
        </button>
"""
    html = re.sub(r'(</nav>\s*)(<a href="img/jibrilresume\.pdf")', r'\1<button id="theme-toggle" aria-label="Toggle Dark Mode" style="background:transparent; border:none; color:var(--text-primary); font-size:2.2rem; cursor:pointer; margin:0 1.5rem; display:flex; align-items:center;">\n          <i class=\'bx bx-sun\'></i>\n        </button>\n        \2', html)

# Inject JS for theme toggle
if "const themeToggle" not in html:
    js_theme_logic = """
      // Theme Toggle Logic
      const themeToggle = document.getElementById('theme-toggle');
      if (themeToggle) {
        const themeIcon = themeToggle.querySelector('i');
        
        const currentTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', currentTheme);
        if(currentTheme === 'light') {
          themeIcon.classList.remove('bx-sun');
          themeIcon.classList.add('bx-moon');
        }

        themeToggle.addEventListener('click', () => {
          let theme = document.documentElement.getAttribute('data-theme');
          if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            themeIcon.classList.remove('bx-sun');
            themeIcon.classList.add('bx-moon');
          } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeIcon.classList.remove('bx-moon');
            themeIcon.classList.add('bx-sun');
          }
        });
      }

      // Mobile menu toggle"""
    html = html.replace("// Mobile menu toggle", js_theme_logic)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("done rewriting index.html")
