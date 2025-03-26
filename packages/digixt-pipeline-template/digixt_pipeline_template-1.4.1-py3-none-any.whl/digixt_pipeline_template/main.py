import argparse
import os
from .project_structure_generator import ProjectStructureGenerator, CommonLogging

def str2bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(
        description='Create a PySpark project structure template',
        usage='%(prog)s -name PROJECT_NAME [--data-migration]'
    )
    parser.add_argument(
        '-name', '--name',
        required=True,
        help='Name of the project (must be at least three characters and a valid Python identifier)'
    )
    
    # Add the --data-migration option
    parser.add_argument(
        '--data-migration', '-data-migration',
        type=str2bool,
        nargs='?',  # This allows the argument to be optional
        const=True,  # If the flag is provided without value, it will default to True
        default=False,  # If the flag is not provided, it will default to False
        help='Enable data migration from database to iceberg table feature for the project (True/False, default: False)'
    )

    args = parser.parse_args()
    project_name = args.name
    is_data_migration = args.data_migration

    
    # validate project name
    if not  (project_name  and len(project_name) >= 3 and project_name.replace('-', '_').isidentifier()):
        raise ValueError("Invalid Project Name: Project Name must be greater than or equal to three in length!")

    logging = CommonLogging.get_logger()
    try:
        logging.info(f"PySpark project structure generator '{project_name}' with data migration set to {is_data_migration}...")
        # logging.info(f"PySpark project structure generator '{project_name}'...")
        ProjectStructureGenerator.copy_and_rename_template(project_name, is_data_migration)
        ProjectStructureGenerator.update_template_script(project_name=project_name, is_data_migration=is_data_migration)
        configs, full_config_file_path = ProjectStructureGenerator.read_config_file(project_name)
        configs = ProjectStructureGenerator.update_template_config(configs, full_config_file_path, project_name, is_data_migration)
        ProjectStructureGenerator.write_to_config_file(configs, full_config_file_path)

        logging.info("Project structore creation complete.")
    except Exception as e:
        logging.error(f"Some thing went wrong while creating the project structure: {str(e)}")
        raise

if __name__ == "__main__":
    main()
