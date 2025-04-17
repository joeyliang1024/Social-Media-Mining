# SMM Assignment

# Assignment 1

In this assignment, you have to to build a crawler that collects data from social media
(e.g. Reddit, FB, Instagram, PTT, Dcard, etc.).
Your data should be relevant to your final project.
*Note: Your data should be based on text data, you're allowed to use other data like image as an aid.

First, you need to discuss the project topic with your teammates, then choose the social media platform you need and crawl your own data.
 
Requirements:
1. Python programming language only.
2. Any library is allowed (Scrapy, Beautifulsoup, Selenium, etc.).
 
Grading:
1. Completed crawler source code.(50%)
2. Please provide 100 sample data. (If your data is not countable, share some examples and provide a brief explanation.) (40%)
3. Brief description of your project topic and the connection between data and project.(10%)
 
Submission rule:
Please pack your source_code.py, sample_data.csv/json and report.pdf into teamid_hw1.zip , and upload it.

# Assignment 2

In this assignment, we will use Pytorch Geometric (PyG) to construct the GCN model and apply it to two OGB (Open Graph Benchmark) public datasets. One dataset will be tasked with Node classification and the other with graph classification.

First, we need the Pytorch Geometric to store the Graph data as a Pytorch Tensor.

*Please do not refer to the related work on the web. But You can discuss your problems with your classmates or TA.

# Assignment 3

In Assignment 3 we constructed GNN models by using PyTorch Geometric built in GCN layer, the `GCNConv`. In this assignment we will implement the **GraphSAGE** ([Hamilton et al. (2017)](https://arxiv.org/abs/1706.02216)) and **GAT** ([Veličković et al. (2018)](https://arxiv.org/abs/1710.10903)) layers directly. Then we will run our models on the CORA dataset, which is a standard citation network benchmark dataset.