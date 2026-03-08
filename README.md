# CSV Processor CLI

A powerful Python CLI tool for processing CSV files with ease.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/csv-processor.git
cd csv-processor

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage

Basic usage:
```bash
csv-processor input.csv output.csv
```

With options:
```bash
csv-processor input.csv output.csv --filter "column > 100" --sort column_name
```

## Features

- **Filter rows** - Apply conditional filters to select specific rows
- **Sort data** - Sort by one or multiple columns
- **Transform columns** - Apply transformations to column values
- **Aggregate data** - Group and aggregate values (sum, avg, count, etc.)
- **Merge files** - Combine multiple CSV files
- **Export formats** - Output to CSV, JSON, or Excel
- **Memory efficient** - Handles large files without loading everything into memory

## Examples

**Filter rows:**
```bash
csv-processor sales.csv filtered.csv --filter "price > 50"
```

**Sort and aggregate:**
```bash
csv-processor data.csv summary.csv --group-by category --aggregate "price:sum"
```

**Transform columns:**
```bash
csv-processor input.csv output.csv --transform "name:upper" --transform "price:round:2"
```

**Merge multiple files:**
```bash
csv-processor --merge file1.csv file2.csv file3.csv --output combined.csv
```

**Export to JSON:**
```bash
csv-processor data.csv --format json --output data.json
```

## Requirements

- Python 3.8+
- pandas
- click

## License

MIT
