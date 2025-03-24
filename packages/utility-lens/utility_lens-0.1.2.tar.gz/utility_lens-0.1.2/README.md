# Utility-Lens
> dev-version 0.1.0c

Is your language model a rational decision maker? Does it consistently prefer \$100 over \$50? Will it still prefer a sandwich over an apple when a banana is available? Can we extract meaningful utility values from its choices?

Utility-Lens helps answer these questions by testing language models against the classical axioms of rational choice theory and extracting underlying utility functions from their revealed preferences.

## Core Analyses

1. **Transitivity**: Does your model make logically consistent choices? 
2. **Independence of Irrelevant Alternatives (IIA)**: Does your model maintain its preferences when new alternatives are introduced?
3. **Utility Estimation**: What cardinal utilities best explain your model's choices?

## Installation

```bash
pip install utility-lens
```

## Demos

### A. Testing Transitivity
Check if your model's preferences form a rational ordering:

<details>
<summary>Code</summary>

```python
from utility_lens import OpenAIModel, TransitivityAnalyzer

# Required: OpenAI API key
openai_api_key = ''

# Required: List of items to compare
animals = [ "elephant", "human", "chimpanzee", "komodo", ...]

###################
# Initialize model#
###################
model = OpenAIModel(
    # Required parameters:
    model_name="gpt-3.5-turbo-0125",  # Required: Name of model to use
    api_key=openai_api_key,           # Required: OpenAI API key

    # Optional parameters (with defaults):
    base_url=None,         # Optional (default=None): Base URL for API 
    max_tokens=10,         # Optional (default=10): Max tokens in response
    concurrency_limit=100, # Optional (default=50): Max concurrent calls
)

#########################
# Initialize analyzer   #
#########################
analyzer = TransitivityAnalyzer(
    # Required parameters:
    model=model,              # Required: Model instance to use
    items=animals,             # Required: List of items to compare

    # Optional parameters (with defaults):
    n_trial=10,             # Optional (default=10): # API calls per pair
                            #  (how many times to ask the same question)
    n_triad=200,            # Optional (default=200): Number of triads
                            # Use -1 for all possible triads
    seed=42,                # Optional (default=42): Random seed
    save_directory="results"# Optional (default=None): Dir to save results
                            # None means don't save results
)

############################
# Run transitivity analysis#
############################
results = analyzer.run(
    use_async=True  # Optional (default=True): Processing mode
                    # True = Concurrent processing (faster but needs async support)
                    # False = Sequential processing (works everywhere)
)

#################################
# Print key transitivity metrics#
#################################
print("\nTransitivity Analysis Results:")
print(f"Overall transitivity score: {results['transitivity_score']:.3f}")
print(f"Weak stochastic transitivity: {results['weak_stochastic_transitivity_satisfied']}")
print(f"Strong stochastic transitivity: {results['strong_stochastic_transitivity_satisfied']}")

# Print top cycles (if any)
print("\nTop preference cycles found:")
for cycle in results['possible_cycles'][:3]:  # Show top 3 cycles
    print(f"\nProbability: {cycle['probability']:.3f}")
    print(f"Path: {cycle['cycle_path']}")
    print(f"Items involved: {cycle['triad']}")

############################################
# Results dictionary structure explanation #
############################################

# Results structure:
# {
#    'transitivity_score': float,    # Overall transitivity (0-1)
#                                   # 1 = perfectly transitive
#                                   # 0 = completely cyclic
#
#    'weak_stochastic_transitivity_satisfied': str,  # Format: "X/Y"
#                                   # X = number of triads satisfying WST
#                                   # Y = total triads tested
#
#    'strong_stochastic_transitivity_satisfied': str,  # Format: "X/Y"
#                                   # X = number of triads satisfying SST
#                                   # Y = total triads tested
#
#    'possible_cycles': List[Dict],  # List of detected preference cycles
#                                   # Sorted by probability (highest first)
#                                   # Each dict contains:
#                                   # - 'probability': float
#                                   # - 'cycle_path': str description
#                                   # - 'triad': List[str] items involved
#
#    'triad_results': List[Dict],   # Detailed results for each triad
#                                   # Including preference strengths and
#                                   # transitivity violations
#
#    'raw_data': List[Dict]         # Raw comparison data from model
# }
```

</details>

### B. Testing IIA
Verify if preferences remain stable with new options:

<details>
<summary>Code</summary>

```python
from utility_lens import OpenAIModel, IIAAnalyzer

# Required: OpenAI API key
openai_api_key = ''

# Required: List of items to compare
animals = [ "elephant", "human", "chimpanzee", "komodo", ...]

###################
# Initialize model#
###################
model = OpenAIModel(
    # Required parameters:
    model_name="gpt-3.5-turbo-0125",  # Required: Name of model to use
    api_key=openai_api_key,           # Required: OpenAI API key

    # Optional parameters (with defaults):
    base_url=None,         # Optional (default=None): Base URL for API 
    max_tokens=10,         # Optional (default=10): Max tokens in response
    concurrency_limit=100, # Optional (default=50): Max concurrent calls
)

#########################
# Initialize analyzer   #
#########################
analyzer = IIAAnalyzer(
    # Required parameters:
    model=model,            # Required: Model instance to use
    items=animals,          # Required: List of items to compare

    # Optional parameters (with defaults):
    n_trial=10,             # Optional (default=10): # API calls per pair
                            #  (how many times to ask the same question)
    n_pairs=-1,             # Default=200: Use 200 out of all possible  
                            #  pairs. Can also use -1 for all pairs or 
                            #  specify a number
    seed=42,                # Optional (default=42): Random seed
    threshold=0.1,          # Optional (default=0.1): IIA threshold
    save_directory="results"# Optional (default=None): Dir to save results
                            # None means don't save results
)

########################
# Run IIA analysis     #
########################
results = analyzer.run(
    use_async=True  # Optional (default=True): Use async processing
)

#########################
# Print IIA metrics     #
#########################
print("\nIIA Analysis Results:")
print(f"Overall IIA score: {results['iia_score_I']:.3f}")

############################################
# Results dictionary structure explanation #
############################################

# Results structure:
# {
#    'iia_score': float,        # Overall IIA satisfaction score (0-1)
#                               # 1 = perfect IIA satisfaction
#                               # 0 = complete IIA violation
#
#    'stable_preferences': int, # Number of pairs with stable preferences
#    'total_pairs': int,        # Total pairs tested
#
#    'violations': List[Dict],  # List of IIA violations
#                               # Sorted by magnitude (largest first)
#                               # Each dict contains:
#                               # - 'base_pair': (str, str)
#                               # - 'original_preference': float
#                               # - 'context_item': str
#                               # - 'new_preference': float
#                               # - 'shift': float
#
#    'pair_results': List[Dict],# Detailed results for each pair
#                               # Including preference strengths
#
#    'raw_data': List[Dict]     # Raw comparison data from model
# }
```

</details>

### C. Extracting Utilities
Compute the underlying utilities that best explain the observed choices:

<details>
<summary>Code - Using Bradley-Terry</summary>

```python
from utility_lens import OpenAIModel, UtilityAnalyzer
import numpy as np

# Required: OpenAI API key
openai_api_key = ''

# Required: List of items to compare
animals = [ "elephant", "human", "chimpanzee", "komodo", ...]

###################
# Initialize model#
###################
model = OpenAIModel(
    # Required parameters:
    model_name="gpt-3.5-turbo-0125",  # Required: Name of model to use
    api_key=openai_api_key,           # Required: OpenAI API key

    # Optional parameters (with defaults):
    base_url=None,        # Optional (default=None): Base URL for API 
    max_tokens=10,        # Optional (default=10): Max tokens in response
    concurrency_limit=100,# Optional (default=50): Max concurrent calls
                          #  Doesn't mean much unless using async
)

#########################
# Initialize analyzer   #
#########################
analyzer = UtilityAnalyzer(
    # Required parameters:
    model=model,            # Required: Model instance to use
    items=animals,          # Required: List of items to compare

    # Optional parameters (with defaults):
    n_trial=10,             # Optional (default=10): # samples per pair 
    n_pairs=-1,             # Default=200: Use 200 out of all possible  
                            #  pairs. Can also use -1 or None for all 
                            #  pairs or specify a number
    seed=42,                # Optional (default=42): Random seed 
    save_directory="results"# Optional (default=None): Set to save 
                            #  None means don't save results
)

################################
# Run Bradley-Terry analysis   #
################################
bt_results = analyzer.run(
    # All parameters are optional with defaults shown:
    method="bradley-terry", # Optional (default="bradley-terry")
                            #  Model type to use
    use_soft_labels=True,   # Optional (default=True): Use ratios vs binary
                            #  True = actual ratios (e.g., 7:3)
                            #  False = binary preferences (e.g., 1 or 0)
    num_epochs=1000,        # Optional (default=1000): Number of training epchs
    learning_rate=0.01,     # Optional (default=0.01): LR for optimization
    use_async=True          # Optional (default=True): Processing mode
                            #  False: Sequential (works everywhere)
                            #  True: Concurrent(faster but needs async support)
)

# Print Bradley-Terry rankings
print("\nBradley-Terry Rankings:")
print(f"Model accuracy: {bt_results['accuracy']:.3f}")
print("\nUtility Rankings:")
for item, utility in bt_results['rankings']:
    print(f"{item}: {utility:.3f}")

############################################
# Results dictionary structure explanation #
############################################

# Bradley-Terry results structure:
# {
#    'utilities': Dict,    # Maps item index to utility value
#                          # Example: {0: 1.2, 1: 0.8, 2: -0.5}
#    'rankings': List,     # Sorted (item, utility) pairs
#                          # Example: [("elephant", 1.2), ("human", 0.8)]
#    'accuracy': float,    # Model prediction accuracy (0-1)
#    'log_loss': float,    # Model log loss
#    'raw_data': Dict      # Raw preference data collected from model
# }

```

</details>

<details>
<summary>Code - Using Thurstonian</summary>

```python
from utility_lens import OpenAIModel, UtilityAnalyzer
import numpy as np

# Required: OpenAI API key
openai_api_key = ''

# Required: List of items to compare
animals = [ "elephant", "human", "chimpanzee", "komodo", ...]

###################
# Initialize model#
###################
model = OpenAIModel(
    # Required parameters:
    model_name="gpt-3.5-turbo-0125",  # Required: Name of model to use
    api_key=openai_api_key,           # Required: OpenAI API key

    # Optional parameters (with defaults):
    base_url=None,        # Optional (default=None): Base URL for API 
    max_tokens=10,        # Optional (default=10): Max tokens in response
    concurrency_limit=100,# Optional (default=50): Max batch size 
                          #  Doesn't mean much unless using async
)

#########################
# Initialize analyzer   #
#########################
analyzer = UtilityAnalyzer(
    # Required parameters:
    model=model,            # Required: Model instance to use
    items=animals,          # Required: List of items to compare

    # Optional parameters (with defaults):
    n_trial=10,             # Optional (default=10): # samples per pair 
    n_pairs=-1,             # Default=200: Use 200 out of all possible  
                            #  pairs. Can also use -1 for all pairs or 
                            #  specify a number
    seed=42,                # Optional (default=42): Random seed 
    save_directory="results"# Optional (default=None): Set to save 
                            #  None means don't save results
)

#############################
# Run Thurstonian analysis  #
#############################
thurst_results = analyzer.run(
    # All parameters are optional with defaults shown:
    method="thurstonian",   # default="bradley-terry": Model type to use
                            #  Model type to use
    use_soft_labels=True,   # Optional (default=True): Use ratios vs binary
                            #  True = actual ratios (e.g., 7:3)
                            #  False = binary preferences (e.g., 1 or 0)
    num_epochs=1000,        # Optional (default=1000): Number of training epchs
    learning_rate=0.01,     # Optional (default=0.01): LR for optimization
    use_async=True          # Optional (default=True): Processing mode
                            #  False: Sequential (works everywhere)
                            #  True: Concurrent(faster but needs async support)
)


# Print Thurstonian rankings with uncertainty
print("\nThurstonian Rankings:")
print(f"Model accuracy: {thurst_results['accuracy']:.3f}")
print("\nUtility Rankings (mean ± std):")
for item, stats in thurst_results['rankings']:
    mean = stats['mean']
    std = np.sqrt(stats['variance'])
    print(f"{item}: {mean:.3f} ± {std:.3f}")

############################################
# Results dictionary structure explanation #
############################################

# Thurstonian results structure:
# {
#    'utilities': Dict,   # Maps item index to mean and variance
#                         # Example: {0: {'mean': 1.2, 'variance': 0.1}}
#    'rankings': List,    # Sorted by mean utility
#                         # Example: [("..", {'mean': 1, 'variance': 1})]
#    'accuracy': float,   # Model prediction accuracy (0-1)
#    'log_loss': float,   # Model log loss
#    'raw_data': Dict     # Raw preference data collected from model
# }

```

</details>