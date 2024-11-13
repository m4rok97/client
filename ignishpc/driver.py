#!/usr/bin/python

import ignis

# Initialization of the framework
ignis.Ignis.start()
# Resources/Configuration of the cluster
prop = ignis.IProperties()
prop["ignis.executor.image"] = "ignishpc/ignishpc"
prop["ignis.executor.instances"] = "1"
prop["ignis.executor.cores"] = "1"
prop["ignis.executor.memory"] = "1GB"
# Construction of the cluster
cluster = ignis.ICluster(prop)

# Initialization of a Python Worker in the cluster
worker = ignis.IWorker(cluster, "python")
# Task 1 - Tokenize text into pairs ('word', 1)
text = worker.textFile("driver.py")
words = text.flatmap(lambda line: [(word, 1) for word in line.split()])
# Task 2 - Reduce pairs with same word and obtain totals
count = words.toPair().reduceByKey(lambda a, b: a + b)
# Print results to file
count.saveAsTextFile("wordcount.txt")

# Stop the framework
ignis.Ignis.stop()
