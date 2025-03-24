from typing import List, Type, Union

"""Generator class for helping iteration of list by split the list and return as list of object"""
class ListSplitter:
    def __init__(self, items: list, batch=10000, as_object=False, dataclass_type: Type = None):
        """
        :param items: List of items to be split.
        :param batch: Batch size.
        :param as_object: Whether to return batches as list or as instances of the given dataclass.
        :param dataclass_type: The dataclass type to be used when returning objects.
        """
        self.items = items
        self.batch = batch
        self.as_object = as_object
        self.dataclass_type = dataclass_type
        self.total_list = len(items)
        self.total_batch = (self.total_list // batch) if self.total_list % batch == 0 else (
                    self.total_list // batch + 1)
        self.current_batch = 0

        if self.as_object and not self.dataclass_type:
            raise ValueError("You must provide a dataclass type when `as_object` is True.")

    def __iter__(self):
        return self

    def __next__(self) -> Union[List, object]:
        if self.current_batch < self.total_batch:
            start = self.current_batch * self.batch
            end = start + self.batch
            self.current_batch += 1
            batch_items = self.items[start:end]

            # Return as either a list or an instance of the input dataclass
            if self.as_object:
                # Create an instance of the provided dataclass with batch items
                return [self.dataclass_type(*item) for item in batch_items]
            return batch_items
        else:
            raise StopIteration