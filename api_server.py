"""
NEPSE Floor Sheet REST API
A simple Flask API to serve CSV data from the /data folder using GitHub API
"""

from flask import Flask, jsonify, request, render_template_string
import pandas as pd
import requests
import base64
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Configuration
GITHUB_REPO_OWNER = "whytofear"  # Replace with your GitHub username
GITHUB_REPO_NAME = "nepse-data-main"        # Replace with your repo name
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')  # Set this in Heroku config vars

class NEPSEDataAPI:
    def __init__(self):
        self.base_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/data"
        self.headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    def get_csv_files(self):
        """Get list of all CSV files from GitHub repo"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            if response.status_code == 200:
                files = response.json()
                csv_files = [f for f in files if f['name'].endswith('.csv')]
                return csv_files
            return []
        except Exception as e:
            print(f"Error fetching CSV files: {str(e)}")
            return []
    
    def get_csv_content(self, filename):
        """Get content of a specific CSV file"""
        try:
            file_url = f"{self.base_url}/{filename}"
            response = requests.get(file_url, headers=self.headers)
            if response.status_code == 200:
                file_info = response.json()
                content = base64.b64decode(file_info['content']).decode('utf-8')
                return content
            return None
        except Exception as e:
            print(f"Error fetching CSV content: {str(e)}")
            return None

# Initialize API
nepse_api = NEPSEDataAPI()

# HTML Template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>📊 NEPSE Floor Sheet API</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            padding: 30px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #4a5568; 
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .api-section { 
            background: #f8f9ff; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }
        .endpoint { 
            background: #e8f4fd; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px;
            border: 1px solid #bee3f8;
        }
        .method { 
            display: inline-block; 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-weight: bold; 
            color: white;
            font-size: 0.8em;
        }
        .get { background: #48bb78; }
        .post { background: #ed8936; }
        code { 
            background: #2d3748; 
            color: #e2e8f0; 
            padding: 15px; 
            border-radius: 5px; 
            display: block; 
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }
        .btn { 
            background: #667eea; 
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 1em;
            margin: 5px;
            transition: all 0.3s ease;
        }
        .btn:hover { 
            background: #5a67d8; 
            transform: translateY(-2px);
        }
        .file-list { 
            max-height: 400px; 
            overflow-y: auto; 
            border: 1px solid #e2e8f0; 
            border-radius: 8px;
        }
        .file-item { 
            padding: 10px; 
            border-bottom: 1px solid #f0f0f0; 
            cursor: pointer;
            transition: background 0.2s ease;
        }
        .file-item:hover { background: #f7fafc; }
        #result { 
            background: #1a202c; 
            color: #e2e8f0; 
            padding: 20px; 
            border-radius: 8px; 
            margin-top: 20px; 
            font-family: monospace;
            max-height: 500px; 
            overflow: auto;
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin: 20px 0;
        }
        .stat-card { 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
        }
        .stat-number { font-size: 2em; font-weight: bold; }
        .stat-label { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 NEPSE Floor Sheet API</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="totalFiles">-</div>
                <div class="stat-label">CSV Files Available</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="latestDate">-</div>
                <div class="stat-label">Latest Data</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalRecords">-</div>
                <div class="stat-label">Total Records</div>
            </div>
        </div>

        <div class="api-section">
            <h2>🚀 Quick Start - Try the API Now!</h2>
            <button class="btn" onclick="listFiles()">📁 List All Files</button>
            <button class="btn" onclick="getLatestData()">📊 Get Latest Data</button>
            <button class="btn" onclick="getStats()">📈 Get Statistics</button>
        </div>

        <div class="api-section">
            <h2>📖 API Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/files</strong> - List all available CSV files
                <code>curl {{ base_url }}/api/files</code>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/data/&lt;filename&gt;</strong> - Get data from specific file
                <code>curl {{ base_url }}/api/data/nepal_stock_floorsheet_2025-06-25.csv</code>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/latest</strong> - Get latest floor sheet data
                <code>curl {{ base_url }}/api/latest</code>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/stats</strong> - Get data statistics
                <code>curl {{ base_url }}/api/stats</code>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/stock/&lt;symbol&gt;</strong> - Get data for specific stock
                <code>curl {{ base_url }}/api/stock/ALBSL</code>
            </div>
        </div>

        <div class="api-section">
            <h2>📁 Available Files</h2>
            <div id="filesList" class="file-list">
                <div style="padding: 20px; text-align: center; color: #666;">
                    Click "List All Files" above to see available data files
                </div>
            </div>
        </div>

        <div class="api-section">
            <h2>📊 API Response</h2>
            <div id="result">
                Click any button above to see API responses here...
            </div>
        </div>
    </div>

<script>
const baseUrl = window.location.origin;

async function apiCall(endpoint) {
    try {
        const response = await fetch(baseUrl + endpoint);
        const data = await response.json();
        document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
        return data;
    } catch (error) {
        document.getElementById('result').innerHTML = 'Error: ' + error.message;
        return null;
    }
}

async function listFiles() {
    const data = await apiCall('/api/files');
    if (data && data.files) {
        let html = '';
        data.files.forEach(file => {
            html += `<div class="file-item" onclick="getData('${file.name}')">
                        📄 ${file.name} 
                        <small style="color: #666; float: right;">${file.size} bytes</small>
                     </div>`;
        });
        document.getElementById('filesList').innerHTML = html;
        document.getElementById('totalFiles').textContent = data.files.length;
    }
}

async function getData(filename) {
    await apiCall(`/api/data/${filename}`);
}

async function getLatestData() {
    const data = await apiCall('/api/latest');
    if (data && data.date) {
        document.getElementById('latestDate').textContent = data.date;
    }
}

async function getStats() {
    const data = await apiCall('/api/stats');
    if (data) {
        document.getElementById('totalRecords').textContent = data.total_records || '-';
        document.getElementById('totalFiles').textContent = data.total_files || '-';
        if (data.latest_date) {
            document.getElementById('latestDate').textContent = data.latest_date;
        }
    }
}

// Load initial data
window.onload = function() {
    listFiles();
    getStats();
};
</script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page with API documentation and interface"""
    base_url = request.url_root.rstrip('/')
    return render_template_string(HTML_TEMPLATE, base_url=base_url)

@app.route('/api/files')
def list_files():
    """List all available CSV files"""
    try:
        files = nepse_api.get_csv_files()
        return jsonify({
            'success': True,
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/data/<filename>')
def get_data(filename):
    """Get data from a specific CSV file"""
    try:
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        content = nepse_api.get_csv_content(filename)
        if content is None:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Convert CSV to JSON
        import io
        df = pd.read_csv(io.StringIO(content))
        
        # Add query parameters support
        limit = request.args.get('limit', type=int)
        stock_symbol = request.args.get('stock')
        
        if stock_symbol:
            df = df[df['Stock Symbol'].str.upper() == stock_symbol.upper()]
        
        if limit:
            df = df.head(limit)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'records': len(df),
            'data': df.to_dict('records')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/latest')
def get_latest():
    """Get the most recent floor sheet data"""
    try:
        files = nepse_api.get_csv_files()
        if not files:
            return jsonify({'success': False, 'error': 'No files found'}), 404
        
        # Sort files by date (assuming filename format includes date)
        latest_file = sorted(files, key=lambda x: x['name'], reverse=True)[0]
        
        content = nepse_api.get_csv_content(latest_file['name'])
        if content is None:
            return jsonify({'success': False, 'error': 'Could not read latest file'}), 500
        
        import io
        df = pd.read_csv(io.StringIO(content))
        
        limit = request.args.get('limit', 50, type=int)
        df = df.head(limit)
        
        return jsonify({
            'success': True,
            'filename': latest_file['name'],
            'date': latest_file['name'].replace('nepal_stock_floorsheet_', '').replace('.csv', ''),
            'records': len(df),
            'data': df.to_dict('records')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get statistics about the data"""
    try:
        files = nepse_api.get_csv_files()
        if not files:
            return jsonify({'success': False, 'error': 'No files found'}), 404
        
        total_records = 0
        dates = []
        stocks = set()
        
        # Sample a few files to get stats (to avoid loading all data)
        sample_files = sorted(files, key=lambda x: x['name'], reverse=True)[:5]
        
        for file_info in sample_files:
            content = nepse_api.get_csv_content(file_info['name'])
            if content:
                import io
                df = pd.read_csv(io.StringIO(content))
                total_records += len(df)
                
                # Extract date from filename
                date_part = file_info['name'].replace('nepal_stock_floorsheet_', '').replace('.csv', '')
                dates.append(date_part)
                
                # Get unique stocks
                if 'Stock Symbol' in df.columns:
                    stocks.update(df['Stock Symbol'].unique())
        
        return jsonify({
            'success': True,
            'total_files': len(files),
            'total_records': total_records,
            'latest_date': max(dates) if dates else None,
            'oldest_date': min(dates) if dates else None,
            'unique_stocks': len(stocks),
            'sample_stocks': list(stocks)[:10]  # First 10 stocks
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    """Get data for a specific stock symbol"""
    try:
        files = nepse_api.get_csv_files()
        if not files:
            return jsonify({'success': False, 'error': 'No files found'}), 404
        
        all_stock_data = []
        
        # Get data from recent files
        recent_files = sorted(files, key=lambda x: x['name'], reverse=True)[:10]
        
        for file_info in recent_files:
            content = nepse_api.get_csv_content(file_info['name'])
            if content:
                import io
                df = pd.read_csv(io.StringIO(content))
                
                # Filter for the specific stock
                stock_data = df[df['Stock Symbol'].str.upper() == symbol.upper()]
                
                if not stock_data.empty:
                    stock_data['Date'] = file_info['name'].replace('nepal_stock_floorsheet_', '').replace('.csv', '')
                    all_stock_data.extend(stock_data.to_dict('records'))
        
        return jsonify({
            'success': True,
            'stock_symbol': symbol.upper(),
            'records': len(all_stock_data),
            'data': all_stock_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
