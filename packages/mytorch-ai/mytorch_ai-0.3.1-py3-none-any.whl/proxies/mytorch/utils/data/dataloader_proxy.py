###############################################################################
# Copyright (c) 2024 MyTorch Systems Inc. All rights reserved.
###############################################################################
from torch.utils.data.Dataset import Dataset


class DataLoaderProxy:
    def __init__(self):
        super().__init__()

    def createDataLoaderOnServer(self, dataset: Dataset, batch_size: int, shuffle: bool):
        """
        Creates a DataLoader instance on the server and returns its UUID and properties
        
        Args:
            dataset: The dataset to load data from
            batch_size: Number of samples per batch
            shuffle: Whether to shuffle the data
            
        Returns:
            tuple: (uuid, dataset_length, batch_size)
        """
        response = self.send_request({
            "command": "create_dataloader",
            "dataset_uuid": dataset.uuid,
            "batch_size": batch_size,
            "shuffle": shuffle
        })
        return response["uuid"], response["dataset_length"], response["batch_size"]

    def getNextDataLoaderBatch(self, batch_index: int):
        """
        Retrieves the next batch of data from the server
        
        Args:
            batch_index: The index of the batch to retrieve
            
        Returns:
            dict: Contains 'inputs' and 'targets' tensors for the batch, or None if no more batches
        """
        response = self.send_request({
            "command": "get_next_batch",
            "batch_index": batch_index
        })
        
        if response.get("end_of_data", False):
            return None
            
        return {
            "inputs": response["inputs"],
            "targets": response["targets"]
        }

# Add this at the end of the file
__all__ = ['DataLoaderProxy']