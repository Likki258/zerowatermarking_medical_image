import torch
import copy

class FederatedServer:
    def __init__(self, global_model_weights):
        self.global_weights = global_model_weights
        self.updates = []

    def receive_update(self, local_weights):
        self.updates.append(local_weights)

    def aggregate_weights(self):
        if not self.updates:
            return self.global_weights

        # Federated Averaging (FedAvg)
        new_weights = copy.deepcopy(self.updates[0])
        for key in new_weights.keys():
            for i in range(1, len(self.updates)):
                new_weights[key] += self.updates[i][key]
            new_weights[key] = torch.div(new_weights[key], len(self.updates))
        
        self.global_weights = new_weights
        self.updates = []
        return self.global_weights

    def get_global_weights(self):
        return self.global_weights
