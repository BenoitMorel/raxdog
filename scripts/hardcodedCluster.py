import clusterRunRaxdog

exampleOptions="/home/morelbt/github/raxdog/data/DataExample/OptionFiles"
exampleResults="/home/morelbt/github/raxdog/results/dataexemplerepeats"

carineOptions="/home/morelbt/github/raxdog/data/DataCarine/OptionFiles"
carineResults="/home/morelbt/github/raxdog/results/datacarinerepeats"

clusterRunRaxdog.writeAndLaunchSubmit(carineOptions, carineResults + "_16", 16)
clusterRunRaxdog.writeAndLaunchSubmit(carineOptions, carineResults + "_128", 128)
clusterRunRaxdog.writeAndLaunchSubmit(carineOptions, carineResults + "_256", 256)
clusterRunRaxdog.writeAndLaunchSubmit(carineOptions, carineResults + "_512", 512)
clusterRunRaxdog.writeAndLaunchSubmit(exampleOptions, exampleResults + "_4", 4)
clusterRunRaxdog.writeAndLaunchSubmit(exampleOptions, exampleResults + "_8", 8)
clusterRunRaxdog.writeAndLaunchSubmit(exampleOptions, exampleResults + "_16", 16)
clusterRunRaxdog.writeAndLaunchSubmit(exampleOptions, exampleResults + "_32", 32)

