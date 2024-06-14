# Q2

基于品类的最优化。

## get D_i first

等效打折率 $D_i$ ：定义 $A_{i_1}$ 与 $A_{i_2}$ 分别作为 $D_i$ 中的打折单品的指标集合与未打折单品集合，则有如下关系得到 $D_i$：
$$
D_i = \frac{ \sum_{(i,j) \in A_{i_1}} p_{i,j} / |A_{i_1}| } { \sum_{(i,j) \in A_{i_2} } p_{i,j} / |A_{i_2}| } 
$$


$$
D_i = \frac{ \sum_{(i,j) \in A_{i_1}} p_{i,j} / |A_{i_1}| } { \sum_{(i,j) \in A_{i_2} } p_{i,j} / |A_{i_2}| } 
$$

为了得到目标时期(2023年6月24-30日)的 $D_i$ ，需要
should get each item $d_{i,j}$ first, then get weighted sum of $D_i$  for $K_i$

for each $g_{i,j}$ get avergae 

$$
d_{i,j} = \frac{ \bar{p}_{i,j}^{(1)} } { \bar{p}_{i,j}^{(2)} }
$$

then for each $K_i$, get weighted sum for $D_i$

$$
D_i = \sum_{i} w_{i,j} d_{i,j}
$$




### make dict_total from goods_ij.xlsx

goods_ij.xlsx is like:

| 单品编码 | 单品名称 | 分类编码 | 分类名称 | i | j |
|---------|---------|---------|---------|---|---|
| 102900005115168 | 牛首生菜 | 1011010101 | 花叶类 | 1 | 1 |


I can build dict_total:  
key is "单品编码", and value is list: ["单品名称", "分类名称", [i,j] ]


###  in DATA2Pre_DiGet1.py 

get primitively prepared data from DATA2.xlsx for later D_i calculation


DATA2 is like:

销售日期	扫码销售时间	单品编码	销量(千克)	销售单价(元/千克)	销售类型	是否打折销售

| 销售日期 | 扫码销售时间 | 单品编码 | 销量(千克) | 销售单价(元/千克) | 销售类型 | 是否打折销售 |
|---------|-------------|---------|------------|------------------|---------|-------------|
| 2020-07-01 | 09:15:07.924 | 102900005117056 | 0.396 | 7.60 | 销售 | 否 |


针对 DATA2.xlsx  首先预处理，drop “销售类型”为“退货”的行（只有462条）。对于剩下的数据进行处理：

我需要提取2023年间06-24至06-30的数据，列为”单品编码“ ”销量(千克)“ ”销售单价(元/千克)“ ”是否打折销售“. then mapping item info.


get preprocessed_DATA2.xlsx, like:

| YearMonthDay | ItemEncode  | singleItemName | category | index_ij | 销量(千克) | 销售单价(元/千克) | 是否打折销售 |
|--------------|-------------|----------------|----------|----------|------------|------------------|-------------|
| 2020-07-01   | 1.029E+14   | 泡泡椒(精品)   | 辣椒类   | [5, 6]   | 0.396      | 7.6              | 否           |




### in DiGet2.py 

further on preprocessed_DATA2.xlsx:

should get $d_{i,j}$ first

对于每一单品，在23年6月24日到6月30日期间


我需要基于”是否打折销售“进行分组，”是“为1组，”否“为2组，然后各组内部按照单品所属类别分组(by i in index_ij)。

use English names for better display in the terminal.

then calculate D_i

through groupby(),  
```python
groups = df.groupby('col1')
df_group - groups.sum()
```











