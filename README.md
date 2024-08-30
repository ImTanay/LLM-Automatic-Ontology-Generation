# Large Language Models for Scholarly Ontology Generation: An Extensive Analysis in the Engineering Field

_This repository is attached to our research paper submitted to the 'Large Language Models and Data Quality for Knowledge Graphs' Special Issue at the Information Processing & Management journal_


## Abstract 
Ontologies of research topics are crucial for structuring scientific knowledge, enabling scientists to navigate vast amounts of research, and forming the backbone of intelligent systems such as search engines and recommendation systems. However, manual creation of these ontologies is expensive, slow, and often results in outdated and overly general representations. As a solution, researchers have been investigating ways to automate or semi-automate the process of generating these ontologies. 
This paper offers a comprehensive analysis of the ability of large language models (LLMs) to identify semantic relationships between different research topics, which is a critical step in the development of such ontologies. To this end, we developed a gold standard based on the IEEE Thesaurus to evaluate the task of identifying four types of relationships between pairs of topics: _broader_, _narrower_, _same-as_, and _other_. Our study evaluates the performance of seventeen LLMs, which differ in scale, accessibility (open vs. proprietary), and model type (full vs. quantised), while also assessing four zero-shot reasoning strategies.
Several models have achieved outstanding results, including Mixtral-8×7B, Dolphin-Mistral-7B, and Claude 3 Sonnet, with F1-scores of 0.847, 0.920, and 0.967, respectively. Furthermore, our findings demonstrate that smaller, quantised models, when optimised through prompt engineering, can deliver performance comparable to much larger proprietary models, while requiring significantly fewer computational resources.

## Info

This repository reports the gold standard and the code we employed to run our experiments
