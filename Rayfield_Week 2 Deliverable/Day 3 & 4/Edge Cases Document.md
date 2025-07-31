# Edge Cases Document
This file lists three possible issues that may happen in the data pipeline and how we will handle them to avoid system failure or incorrect results.

### 1. Unexpected Column Changes
**What might happen:**  
A new column might appear in the dataset, or an existing column name might be changed or removed.

**How the pipeline will handle it:**  
> Add a column validation step at the start of the script  
> Compare column names with an expected list  
> If a mismatch is found, stop the pipeline and log an error message  
> Allow easy updating of expected columns through a config file

### 2. Missing Data for a Whole Day
**What might happen:**  
Some days (like holidays or system outages) might have no recorded data.

**How the pipeline will handle it:**  
> Use a complete time index and reindex the dataset  
> Fill missing values using forward fill (`ffill`) or mark them with NaN  
> Create a new column to indicate missing entries  
> Document these gaps in the log file for review

### 3. Multiple Site Support / Scaling
**What might happen:**  
The pipeline may need to handle data from multiple solar sites in the future.

**How the pipeline will handle it:**  
> Design the script to loop over multiple input files (one per site)  
> Output cleaned data into site-specific folders (e.g., `data_cleaned/site_A.csv`)  
> Store results in a structured directory  
> Use parameterized functions for each processing step