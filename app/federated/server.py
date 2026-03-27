import torch
import numpy as np
from typing import List, Dict

class FederatedServer:
    def __init__(self):
        self.global_weights = None
        self.active_nodes = 0

    def aggregate_updates(self, local_weights_list: List[Dict[str, torch.Tensor]]):
        """
        Implements Federated Averaging (FedAvg).
        """
        if not local_weights_list:
            return None

        # Initialize global weights with the structure of the first local update
        if self.global_weights is None:
            self.global_weights = {k: torch.zeros_like(v) for k, v in local_weights_list[0].items()}

        # Simple average of weights
        n = len(local_weights_list)
        for key in self.global_weights.keys():
            sum_weights = sum(local_weights[key] for local_weights in local_weights_list)
            self.global_weights[key] = sum_weights / n
            
        print(f"Successfully aggregated updates from {n} hospital nodes.")
        return self.global_weights

    def get_global_model(self):
        return self.global_weights
