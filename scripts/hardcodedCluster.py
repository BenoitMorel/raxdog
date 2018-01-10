import clusterRunRaxdog

exampleOptions="/home/morelbt/github/raxdog/data/DataExample/OptionFiles"
exampleResults="/home/morelbt/github/raxdog/results/dataexemplerepeats"

carineOptions="/home/morelbt/github/raxdog/data/DataCarine/OptionFiles"
carineResults="/home/morelbt/github/raxdog/results/datacarinerepeats"

clusterRunRaxdog.writeAndLaunchSubmit(carineOptions, carineResults + "_128", 128)
#clusterRunRaxdog.writeAndLaunchSubmit(exampleOptions, exampleResults, 4)

