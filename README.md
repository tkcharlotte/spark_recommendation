## spark_recommendation

基于spark的协同过滤算法ALS的实现demo

考虑到后期数据可视化的因素，采python的pyspark模块来实现，后期可视化使用web框架flask，前遍历输出推荐的电影名。

extract.py : 提取数据集中的user字段进行保存，用来判断用户ID是否存在，达到在输入ID之后立即产生结果，而不是在运行算法的时候才捕捉异常，再输出。