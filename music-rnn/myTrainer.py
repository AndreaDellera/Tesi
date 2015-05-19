from pybrain.utilities import Named, abstractMethod


class myTrainer(Named):
    """ A trainer determines how to change the adaptive parameters of a module. 
    It requires access to a DataSet object (which provides input-target tuples). """
    # e.g. bptt, rtrl, svm
    
    ds = None
    module = None
    
    def __init__(self, module):
        self.module = module    
    
    def setData(self, dataset):
        """Associate the given dataset with the trainer."""
        self.ds = dataset
        if dataset:
            assert dataset.indim == self.module.indim
            assert dataset.outdim == self.module.outdim
        
    def trainOnDataset(self, dataset, *args, **kwargs):
        """Set the dataset and train. 
        
        Additional arguments are passed on to the train method."""
        self.setData(dataset)
        return self.trainEpochs(*args, **kwargs)
        
    def trainEpochs(self, epochs=1, *args, **kwargs):
        """Train on the current dataset for the given number of `epochs`. 
        
        Additional arguments are passed on to the train method."""
        errors = []
        for dummy in range(epochs):
            errors.append(self.train(*args, **kwargs))
        return errors
        
    def train(self):
        """Train on the current dataset, for a single epoch."""
        abstractMethod()

        
