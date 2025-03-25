# vikdatashift

vikdatashift is a Python package designed to facilitate data migration between CSV files and databases (Oracle and PostgreSQL), as well as between different database systems.

## Version 0.1 Features

- Import data from CSV files to Oracle or PostgreSQL databases
- Create tables in the target database based on CSV structure
- Truncate existing tables before data insertion (optional)
- Efficient data loading using chunked processing

## Installation

You can install vikdatashift using pip:

```bash
pip install vikdatashift