# Snailz

<img src="https://raw.githubusercontent.com/gvwilson/snailz/main/img/snail-logo.svg" alt="snail logo" width="200px">

These synthetic data generators model genomic analysis of snails in
the Pacific Northwest that are growing to unusual size as a result of
exposure to pollution.

-   A *grid* is created to record the *pollution levels* at a sampling site.
-   One or more *specimens* are collected from the grid.
    Each specimen has a *genome* and a *mass*.
-   *Laboratory staff* design and perform *assays* of those genomes.
-   Each assay is represented by a *design file* and an *assay file*.
-   Assay files are mangled to create *raw* files with formatting glitches.

## Usage

1.  Create a fresh Python environment: `uv venv`
2.  Activate that environment: `source .venv/bin/activate`
3.  Install dependencies and editable version of package: `uv pip install -e '.[dev]'`
4.  View available commands: `doit list` or `snailz --help`
6.  Regenerate all data in `./tmp` using parameters in `./params`: `doit all`

<img src="https://raw.githubusercontent.com/gvwilson/snailz/main/img/workflow.png" alt="workflow">

## Parameters

`./params` contains the parameter files used to control generation of the reference dataset.

-   `grid.json`
    -   `depth`: integer range of random values in cells
    -   `seed`: RNG seed
    -   `size`: width and height of (square) grid in cells
-   `people.json`
    -   `locale`: language and region to use for name generation
    -   `number`: number of staff to create
    -   `seed`: RNG seed
-   `specimens.json`
    -   `length`: genome length in characters
    -   `max_mass`: maximum specimen mass
    -   `min_mass`: minimum specimen mass
    -   `mut_scale`: scaling factor for mutated specimens
    -   `mutations`: number of mutations to introduce
    -   `number`: number of specimens to create
    -   `seed`: RNG seed
-   `assays.json`
    -   `baseline`: assay response for unmutated specimens
    -   `end_date`: date of final assay
    -   `mutant`: assay response for mutated specimens
    -   `noise`: noise to add to control cells
    -   `plate_size`: width and height of assay plate
    -   `seed`: RNG seed
    -   `start_date`: date of first assay

Note: there are no parameters for assay file mangling.

## Data Dictionary

`doit all` creates these files in `tmp` using the sample parameters in `params`:

-   `assays/`
    -   `NNNNNN_assay.csv`: tidy, consistently-formatted CSV file with assay result.
    -   `NNNNNN_design.csv`: tidy, consistently-formatted CSV file with assay design.
    -   `NNNNNN_raw.csv`: CSV file derived from `NNNNNN_assay.csv` with randomly-introduced formatting errors.
-   `assays.csv`: CSV file containing summary of assay metadata with columns.
    -   `ident`: assay identifier (integer).
    -   `specimen_id`: specimen identifier (text).
    -   `performed`: assay date (date).
    -   `performed_by`: person identifier (text).
-   `assays.json`: all assay data in JSON format.
-   `grid.csv`: CSV file containing pollution grid values.
    -   This file is a matrix of values with no column IDs or row IDs.
-   `grid.json`: grid data as JSON.
-   `people.csv`: CSV file describing experimental staff members.
    -   `ident`: person identifier (text)
    -   `personal`: personal name (text)
    -   `family`: family name (text)
-   `people.json`: staff member data in JSON format.
-   `specimens.csv`: CSV file containing details of snail specimens.
    -   `ident`: specimen identifier (text)
    -   `x`: X coordinate of collection cell (integer)
    -   `y`: Y coordinate of collection cell (integer)
    -   `genome`: base sequence (text)
    -   `mass`: snail mass (real)
-   `specimens.json`: specimen data in JSON format.
