# Improving Graph Neural Networks for Multimodal Data
 These days, session based recommendation is common across many e-commerce plat
forms and other websites where user behind the session is anonymous, yet it aims
 to predict his further interactions. There have already been many studies trying to
 solve the problem, one particular class of them models each session as graph and ap
plies a Graph Neural Network (GNN) to capture session’s preference and return list
 of recommendations. In this thesis we propose on how to improve efficiency of those,
 by identifying information regarding multimodal nature of sessions. With use of
 Gaussian Mixtures we analyse user’s behaviour and provide insight into what we as
sume is multimodality in case of session data. Suggested solution introduces method
 of applying extracted knowledge into the GNN at its core by modifying adjacency
 matrix of each session graph, greatly improving quality of recommendations.

# Paper
Full work attached as PDF.

# Source Code
Python source code organized with help of `poetry` framework, as well as some notebooks with potential usage and analysis of results.
Code based on https://github.com/CRIPAC-DIG/SR-GNN/tree/master, updated with newer version of `torch` as well as `pytorch-lightning`.

# Weights & Biases
W&B project with all experiments I have ran over the course developing the thesis. Quite messy
https://wandb.ai/kpuchalskixiv/GNN_master?workspace=user-kpuchalskixiv
