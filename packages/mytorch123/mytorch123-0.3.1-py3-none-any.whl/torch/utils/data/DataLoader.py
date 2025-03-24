###############################################################################
# Copyright (c) 2024 MyTorch Systems Inc. All rights reserved.
###############################################################################
from torch.utils.data.Dataset import Dataset
from proxies.mytorch.utils.data.dataloader_proxy import DataLoaderProxy


class DataLoader:
    def __init__(self, dataset: Dataset, batch_size: int, shuffle: bool) -> None:
        super().__init__()
        self.dataset = dataset
        self.shuffle = shuffle
        self.proxy = DataLoaderProxy()
        self.uuid, self.dataset_length, self.batch_size = self.createDataLoaderOnServer(dataset, batch_size, shuffle)
        self.batch_index = 0  # Initialize batch index

    def createDataLoaderOnServer(self, dataset: Dataset, batch_size: int, shuffle: bool):
        uuid, dataset_length, batch_size = self.proxy.createDataLoaderOnServer(dataset, batch_size, shuffle)
        return uuid, dataset_length, batch_size

    def __len__(self):
        return self.dataset_length

    # When we loop through the batches of a DataLoader, we will call this method to get the next batch
    # of data from the DataLoaderProxy, which gets it from the DataLoader on the server
    def __iter__(self):
        self.batch_index = 0  # Reset at the start of each iteration
        return self

    def __next__(self):
        next_batch = self.proxy.getNextDataLoaderBatch(self.batch_index)
        if next_batch is None:  # Or any other condition indicating no more data
            raise StopIteration
        self.batch_index += 1  # Increment for the next request
        # next batch is a tuple of two Tensors: the input data and the target (label) data
        return next_batch["inputs"], next_batch["targets"]

# Export everything from this module
__all__ = ['DataLoader']
