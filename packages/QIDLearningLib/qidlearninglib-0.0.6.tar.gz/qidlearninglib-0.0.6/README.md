# QIDLearningLib: A Python Library for Quasi-Identifier Recognition and Evaluation

![Python 3.8+](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![PyPI version](https://badge.fury.io/py/QIDLearningLib.svg)
![Build Status](https://github.com/smartlord7/QIDLearningLib/workflows/Build/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-95%25-green.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

QIDLearningLib is the first comprehensive Python library designed for automated quasi-identifier (QID) recognition and evaluation in tabular datasets. It integrates metrics from causality, data privacy, and data utility to provide a holistic assessment of potential QIDs, enabling systematic identification and mitigation of privacy risks in data sharing and analysis.  

The implemented metrics can be used flexibly within the provided optimization algorithms—including evolutionary algorithms, simulated annealing, and greedy search—to automatically select QIDs that balance data privacy and utility. This ensures that users can tailor the selection process based on their specific needs, optimizing privacy protection while preserving data usability.


## Key Features

- Integration of metrics from causality, data privacy, and data utility domains designed for QID selection
- Support for multiple optimization algorithms including evolutionary algorithms, simulated annealing, and greedy search for automated QID selection
- Redundancy analysis to identify the most relevant, non-overlapping metrics
- Graphical and testing tools for metrics' enhanced interpretability
- Evaluation metrics to assess the performance of QID selection systems against ground-truth
- Compliance with regulatory frameworks like GDPR

## Installation

bash
pip install QIDLearningLib


## Quick Usage Example

python
import pandas as pd
from QIDLearningLib.optimizer.ea import EvolutionaryAlgorithm
from QIDLearningLib.metrics.performance import recall, specificity, accuracy

# Load your dataset
df = pd.read_csv("your_dataset.csv")

# Define metrics for optimization
metrics = [
    {"name": "Distinction", "weight": 0.25, "maximize": True},
    {"name": "Separation", "weight": 0.25, "maximize": True},
    {"name": "k-Anonymity", "weight": -0.4, "maximize": True},
    {"name": "Delta Distinction", "weight": 0.2, "maximize": True},
    {"name": "Delta Separation", "weight": 0.2, "maximize": True},
    {"name": "Attribute Length Penalty", "weight": -1, "maximize": True}
]

# Configure and run the evolutionary algorithm
ea = EvolutionaryAlgorithm(df, metrics, population_size=50, generations=30)
best_individual, best_fitness, history = ea.run()

# Retrieve selected QIDs
selected_attributes = df.columns[best_individual == 1]

# Evaluate performance against ground truth (if available)
ground_truth_qids = {"Age", "Gender", "Zipcode"}  # Example ground truth
recall_score = recall(selected_attributes, ground_truth_qids)
specificity_score = specificity(selected_attributes, ground_truth_qids)
accuracy_score = accuracy(selected_attributes, ground_truth_qids)


## Metrics

### Causality Metrics
- **Covariate Shift**: Quantifies distribution differences between treated and control groups
- **Balance Test**: Assesses balance between treated and control groups
- **Propensity Overlap**: Evaluates overlap in propensity scores
- **Causal Importance**: Measures causal relationships involving QIDs

### Data Privacy Metrics
- **k-Anonymity**: Measures indistinguishability of records
- **l-Diversity**: Quantifies diversity of sensitive attributes within groups
- **t-Closeness**: Evaluates divergence from dataset-wide sensitive distributions
- **𝛿-Presence**: Measures inference risk of sensitive attributes
- **Generalization Ratio**: Assesses distribution variation

### Data Utility Metrics
- **Mean Squared Error (MSE)**: Average squared prediction error
- **Accuracy**: Proportion of correct predictions
- **Range Utility**: Range of values within groups
- **Distinct Values Utility**: Number of unique values
- **Completeness Utility**: Proportion of non-null values
- **Group Entropy**: Randomness within QID groups
- **Information Gain**: Reduction in entropy of target attribute
- **Gini Index**: Impurity of target attribute within groups
- **Attribute Length Penalty**: Balances QID selection

### QID-Specific Metrics
- **Distinction**: Ratio of unique QID values
- **Separation**: Separability of records based on QIDs

### Performance Metrics
- Precision
- Recall
- F1 Score
- Jaccard Similarity
- Specificity
- False Positive Rate
- Dice Similarity Coefficient
- F-Beta Score

## Functionalities

- **Automated QID Recognition**: Uses optimization algorithms to identify optimal QID combinations
- **Metric Calculation**: Computes various metrics across different domains
- **Redundancy Analysis**: Identifies relevant and non-overlapping metrics
- **Visualization Tools**: Generates graphs to inspect metric distributions
- **Performance Evaluation**: Compares predicted QIDs against ground truth
- **Educational Resources**: Provides tools for understanding data privacy concepts

## Optimization Algorithms

- **Evolutionary Algorithm**: Bio-inspired approach for iterative refinement of QID combinations
- **Tabu Search**: Metaheuristic optimization with memory structures
- **Greedy Search**: Locally optimal choices at each step
- **Simulated Annealing**: Probabilistic technique for global optimization

## Contributing

Contributions are welcome! Please see our [contribution guidelines](https://github.com/smartlord7/QIDLearningLib/blob/main/CONTRIBUTING.md) for details.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

## Acknowledgments

This work is partially financed through national funds by FCT - Fundação para a Ciência e a Tecnologia, I.P., in the framework of the Project UIDB/00326/2025 and UIDP/00326/2025.

For more information, please visit the [official GitHub repository](https://github.com/smartlord7/QIDLearningLib).