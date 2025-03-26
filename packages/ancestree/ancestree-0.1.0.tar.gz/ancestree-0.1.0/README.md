# GWAS Toolkit

A comprehensive Python package for processing and analyzing Genome-Wide Association Study (GWAS) data.

## Features

- Data import/export for common GWAS file formats
- Quality control and filtering of genetic variants
- Population stratification correction
- Association testing with various statistical models
- Visualization of GWAS results
- Annotation and functional interpretation of significant variants

## Installation

```bash
pip install gwas_toolkit
```

## Usage

```python
import gwas_toolkit as gtk

# Load GWAS data
data = gtk.load_data("path/to/gwas_data.txt")

# Perform quality control
filtered_data = gtk.quality_control(data, maf=0.05, geno=0.1, hwe=1e-6)

# Run association analysis
results = gtk.run_association(filtered_data, model="linear")

# Visualize results
gtk.manhattan_plot(results)
gtk.qq_plot(results)

# Annotate significant variants
annotated = gtk.annotate_variants(results.significant())
```

## Documentation

For detailed documentation, visit [docs.gwastoolkit.org](https://docs.gwastoolkit.org).

## Requirements

- Python ≥ 3.8
- numpy
- pandas
- scipy
- matplotlib
- statsmodels
- scikit-learn

## License

MIT 