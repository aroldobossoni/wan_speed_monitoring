import speedtest
import json
from datetime import datetime
import os
import sys

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def test_speed():
    try:
        print("Starting speed test...")
        
        config = load_config()
        
        # Initialize speedtest
        st = speedtest.Speedtest()
        
        if config and config.get('id'):  # Check if config exists and has server id
            print(f"Selected server: {config['sponsor']} - {config['name']}")
            # Set the chosen server with all information from config
            server = config.copy()
            st.servers = [server]
            st._best = server
        else:
            print("Configuration not found or server not specified.")
            print("Getting best server automatically...")
            st.get_best_server()
            # Save server info for display
            config = {
                'name': st._best['name'],
                'sponsor': st._best['sponsor'],
                'country': st._best['country']
            }
        
        print("Testing download speed...")
        download_speed = st.download()
        
        print("Testing upload speed...")
        upload_speed = st.upload()
        
        print("Getting ping...")
        ping = st.results.ping
        
        print("Getting jitter...")
        jitter = st.results.ping_jitter if hasattr(st.results, 'ping_jitter') else 0
        
        results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'download': round(download_speed, 2),
            'upload': round(upload_speed, 2),
            'ping': round(ping),
            'jitter': round(jitter)
        }
        
        return results
        
    except Exception as e:
        print(f"Error performing speed test: {str(e)}")
        return None

def generate_html(results, config):
    """Generate HTML content with test results"""
    return f"""
    <html>
    <head>
        <title>Speed Test Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 10px; }}
            .result {{ margin-bottom: 5px; }}
            .server {{ color: #666; }}
        </style>
    </head>
    <body>
        <h2>Test Results - {results['timestamp']}</h2>
        <div class="server">
            Server: {config.get('sponsor')} - {config.get('name')}
        </div>
        <div class="result">
            Download: {results['download'] / 1_000_000:.2f} Mbps
        </div>
        <div class="result">
            Upload: {results['upload'] / 1_000_000:.2f} Mbps
        </div>
        <div class="result">
            Ping: {results['ping']} ms
        </div>
        <div class="result">
            Jitter: {results['jitter']} ms
        </div>
    </body>
    </html>
    """

def save_results(results):
    if results is None:
        return
        
    # Load config to get server information
    config = load_config()
    if config is None:
        print("Configuration file not found.")
        return
    
    # Generate and save HTML content
    html_content = generate_html(results, config)
    filename = 'results.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Results saved to", filename)
    
    # Display results
    print("\nTest Results:")
    print(f"Server: {config.get('sponsor')} - {config.get('name')}")
    print(f"Download: {results['download'] / 1_000_000:.2f} Mbps")
    print(f"Upload: {results['upload'] / 1_000_000:.2f} Mbps")
    print(f"Ping: {results['ping']} ms")
    print(f"Jitter: {results['jitter']} ms")

def main():
    results = test_speed()
    if results:
        save_results(results)
    else:
        print("Unable to complete speed test.")

if __name__ == "__main__":
    main()
