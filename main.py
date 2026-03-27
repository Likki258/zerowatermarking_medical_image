import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.flask_app import app

def start_platform():
    print("🚀 Starting Blockchain-Anchored Federated Zero-Watermarking Platform...")
    print("📡 Federated Nodes: Simulated Hospital Swarm Active")
    print("🔗 Blockchain: Immutable Ledger Initialized")
    print("----------------------------------------------------------------------")
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    start_platform()
