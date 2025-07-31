# Annotated Diagram Notes
This file explains each step in my pipeline diagram. For each part, I have described the tool, when it runs, and what files or data it uses.

### 1. Input: CSV File (Raw Data)
**Tool used:** Manual file upload or script that pulls from online source (e.g. Kaggle)
**Trigger:** Manual upload (user provides the file)
**Input:** `solar_data_raw.csv`
**Output:** Raw file loaded into memory (DataFrame)

### 2. Load Data with Pandas
**Tool used**: Python with `pandas` library
**Trigger**: Runs once when script is started
**Input**: `solar_data_raw.csv`
**Output**: In-memory DataFrame (not saved yet)

### 3. Clean Data
**Tool used**: Pandas
**Trigger**: Part of main script
**Tasks**: (below)
> Drop or fill missing values
> Rename columns to readable names
> Convert units (e.g., MWh to kWh)
>Convert time column to `datetime` format

**Input**: Raw DataFrame
**Output**: Cleaned DataFrame

### 4. Create New Data Columns (Feature Engineering)
**Tool used**: Pandas
**Trigger**: After cleaning is complete
**Tasks**:
> Calculate 7-day rolling average
> Compute hourly or daily percentage change
> Find time since last peak output

**Input**: Cleaned DataFrame
**Output**: Enhanced DataFrame with new columns

### 5. Save Cleaned Output
**Tool used**: Pandas `.to_csv()`
**Trigger**: End of processing step
**Input**: Enhanced DataFrame
**Output**: `cleaned_data.csv` (used in ML or visualization later)

### 6. Visualization (Optional)
**Tool used**: Matplotlib or Seaborn
**Trigger**: Manual or part of notebook
**Input**: Cleaned DataFrame
**Output**: Line chart, histogram (shown in notebook)