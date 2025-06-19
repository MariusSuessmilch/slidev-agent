#!/bin/bash
set -e

echo "🚀 Building Slidev Agent Demo Site..."

# Clean previous builds
rm -rf demo dist
mkdir -p demo dist

echo "📄 Generating demo presentations..."

# Generate demo presentations (requires OPENAI_API_KEY)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set, skipping demo generation"
    echo "Set OPENAI_API_KEY environment variable to generate live demos"
    
    # Create placeholder index
    cp index.html dist/
    echo "✅ Basic site built (without demos)"
    exit 0
fi

# Generate multiple demo presentations
echo "🐍 Generating Python Functions demo..."
uv run python -m slide_agent.cli "Python Functions" --audience "students" --slide-count 6 --language "en" --output-dir "demo/python-functions"

echo "🤖 Generating Machine Learning demo..."
uv run python -m slide_agent.cli "Machine Learning Grundlagen" --audience "Studenten" --slide-count 7 --language "de" --output-dir "demo/machine-learning"

echo "🌐 Generating Web Development demo..."
uv run python -m slide_agent.cli "Web Development Basics" --audience "beginners" --slide-count 5 --language "en" --output-dir "demo/web-development"

echo "📝 Creating demo index page..."

# Create main demo index page
cat > demo/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slidev Agent - Demo Presentations</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        .header h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .presentations {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        .presentation-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .presentation-card:hover {
            transform: translateY(-5px);
        }
        .view-btn {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            text-decoration: none;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎛️ Slidev Agent</h1>
        <p>AI-powered slide generation using LangGraph and OpenAI GPT-4o</p>
    </div>

    <div class="presentations">
        <div class="presentation-card">
            <h3>🐍 Python Functions</h3>
            <p>Introduction to Python functions for students.</p>
            <a href="./python-functions/" class="view-btn">View Presentation →</a>
        </div>

        <div class="presentation-card">
            <h3>🤖 Machine Learning Grundlagen</h3>
            <p>Einführung in maschinelles Lernen (Deutsch).</p>
            <a href="./machine-learning/" class="view-btn">Präsentation anzeigen →</a>
        </div>

        <div class="presentation-card">
            <h3>🌐 Web Development Basics</h3>
            <p>Essential web development concepts for beginners.</p>
            <a href="./web-development/" class="view-btn">View Presentation →</a>
        </div>
    </div>
</body>
</html>
EOF

echo "🔧 Building Slidev presentations..."

# Build each presentation
echo "Building Python Functions..."
cd slides/presentation-python-functions
npm install --silent
npm run build
cd ../..

echo "Building Machine Learning..."
cd slides/presentation-machine-learning-grundlagen  
npm install --silent
npm run build
cd ../..

echo "Building Web Development..."
cd slides/presentation-web-development-basics
npm install --silent
npm run build
cd ../..

echo "📦 Setting up final build directory..."

# Copy main index
cp demo/index.html dist/

# Copy presentation builds
mkdir -p dist/python-functions
cp -r slides/presentation-python-functions/dist/* dist/python-functions/

mkdir -p dist/machine-learning
cp -r slides/presentation-machine-learning-grundlagen/dist/* dist/machine-learning/

mkdir -p dist/web-development
cp -r slides/presentation-web-development-basics/dist/* dist/web-development/

echo "✅ Build complete! Demo site available in ./dist/"
echo "🌐 Open dist/index.html in your browser to view"
echo ""
echo "To serve locally:"
echo "  cd dist && python -m http.server 8000"
echo "  Then open http://localhost:8000"