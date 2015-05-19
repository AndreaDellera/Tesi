from pybrain.structure import SigmoidLayer, TanhLayer, LinearLayer
# from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from myBackProp import myBackpropTrainer
import matplotlib.pyplot as mpl




get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

def main():

    ds = SupervisedDataSet(2, 1)

    for i in range(2):
        for j in range(2):
            ds.addSample((bool(i), bool(j)), (bool(i) != bool(j)))

    for inpt, target in ds:
        print inpt, target

    net = buildNetwork(ds.indim, 6, 6, ds.outdim, recurrent=True, outclass=LinearLayer, hiddenclass=SigmoidLayer)
    trainer = myBackpropTrainer(net, dataset=ds, learningrate = 0.01, momentum = 0.99) # if verbose == True then print "Total error:", errors / ponderation

    # training the network
    print "start training"

    x = trainer.trainOnDataset(ds, 1000)


    print "finish training"

    trainer.testOnData(verbose= True)
    mpl.plot(range(len(x)), x)
    mpl.show()


if __name__ == "__main__":
    main()