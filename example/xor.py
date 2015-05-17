import xml.etree.ElementTree as ET
import glob
from pybrain.structure import RecurrentNetwork
from pybrain.structure import SigmoidLayer, TanhLayer, LinearLayer
from pybrain.structure import FullConnection
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.tools.validation    import testOnSequenceData
from pybrain.tools.shortcuts import buildNetwork


get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

def main():

    ds = SupervisedDataSet(2, 1)

    for i in range(2):
        for j in range(2):
            ds.addSample((bool(i), bool(j)), (bool(i) != bool(j)))

    for inpt, target in ds:
        print inpt, target

    net = buildNetwork(ds.indim, 6, ds.outdim, hiddenclass=TanhLayer, outclass=LinearLayer, outputbias=False, recurrent=True)

    trainer = BackpropTrainer(net)
    # training the network
    print "start training"

    trainer.trainOnDataset(ds, 1000)


    print "finish training"

    trainer.testOnData(verbose= True)



if __name__ == "__main__":
    main()