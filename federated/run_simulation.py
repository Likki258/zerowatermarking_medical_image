import torch
from federated.model_wrapper import FederatedResNet
from federated.server import FederatedServer
import time

def run_federated_round(num_nodes=3):
    print(f"Starting Federated Learning Round with {num_nodes} hospital nodes...")
    
    # Initialize global model wrapper
    global_wrapper = FederatedResNet()
    global_weights = global_wrapper.get_weights()
    
    # Initialize server
    server = FederatedServer(global_weights)
    
    # Simulate nodes
    nodes = [FederatedResNet() for _ in range(num_nodes)]
    
    # Synchronize nodes with global model
    for node in nodes:
        node.set_weights(global_weights)
        
    print("Nodes synchronized with global ResNet-50 weights.")
    
    # Simulate local training
    for i, node in enumerate(nodes):
        print(f"Hospital Node {i+1} training on local clinical images...")
        # In a real scenario, we would use a local DataLoader here
        # For simulation, we'll just perturb the weights slightly to simulate training
        local_weights = node.get_weights()
        for key in local_weights.keys():
            local_weights[key] += torch.randn(local_weights[key].size()) * 0.0001
        
        server.receive_update(local_weights)
        time.sleep(0.5)
        
    print("All updates received by central server. Aggregating...")
    new_global_weights = server.aggregate_weights()
    
    # Update global model
    global_wrapper.set_weights(new_global_weights)
    print("Global model updated successfully via Federated Averaging.")
    
    return global_wrapper

if __name__ == "__main__":
    run_federated_round()
