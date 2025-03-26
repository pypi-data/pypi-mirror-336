# Digixt Pipeline Template Plugin Builder

## Overview
The Digixt Pipeline Template Plugin Builder is a tool designed to help you quickly set up PySpark projects with a predefined structure. It automates the creation of a project directory with necessary templates and configuration files, making it easier to get started with PySpark development.

## Features
## Features

- **Automated Project Structure**: Generates a standardized project directory with predefined directories and files, ensuring a consistent starting point for new PySpark projects.
- **Automated Data Migration Setup**: Generates a project structure specifically tailored for data migration from a database to Iceberg tables, including necessary configurations and files for seamless integration.
- **Customizable Configuration:** Supports the customization of project settings through configuration files, allowing adjustments to match specific project requirements.
- **Enhanced Functionality:** Offers enriched functions that assist Data Engineers in developing and managing PySpark pipelines efficiently.
- **Ease of Use:** Simplifies the setup process for new projects, reducing manual configuration and setup time.

## Installation
To install the plugin, use pip:

```pip install digixt-pipeline-template```

## Packaging manually on local (optional).


## Usage
To create a new PySpark project structure, run:

```digixt-pipeline-template --name <my-project-name> [-data-migration]```

Also, user can run  help command.

``` digixt-pipeline-template --help ```

Replace ```<my-project-name>``` with your desired project name.
