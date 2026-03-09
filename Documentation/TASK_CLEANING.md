# Text Preprocessing Pipeline

## Overview

This project implements a **configurable text preprocessing pipeline** for cleaning and preparing scraped review datasets.
The script dynamically loads multiple CSV files from a folder and applies optional preprocessing steps using command-line arguments.

The pipeline supports:

* Lowercasing text
* Removing URLs
* Removing special characters
* Lemmatization
* Regex-based category extraction

---

## Project Structure

```
project/
│
├── cleaning.py
├── README.md
│
├── data/
│   ├── file1.csv
│   ├── file2.csv
│   └── file3.csv
```

---

## Requirements

* Python 3.8+
* pandas
* textblob
* nltk

---

## Installation

### 1. Clone the repository (or download the project)

```
git clone <your-repo-url>
cd project
```

### 2. Create a virtual environment

```
python3 -m venv venv
```

### 3. Activate the virtual environment

Linux / macOS:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

### 4. Install required packages

```
pip install pandas textblob nltk
```

### 5. Download TextBlob corpora

```
python -m textblob.download_corpora
```

---

## Usage

Run the preprocessing pipeline:

```
python cleaning.py data
```

You can enable additional preprocessing steps using flags:

```
python cleaning.py data --lowercase --remove_urls --remove_special --lemmatize --extract_tags
```

---

## Output

The cleaned dataset will be saved as:

```
clean_data.csv
```

---

## Features

* Dynamic loading of multiple CSV files
* Modular preprocessing functions
* Command-line configurable pipeline
* Regex-based categorization

---

## Author

Abdelrahman Hassan Metwally
