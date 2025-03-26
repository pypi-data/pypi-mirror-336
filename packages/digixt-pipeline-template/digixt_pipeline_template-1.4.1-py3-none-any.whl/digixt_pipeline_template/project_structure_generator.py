import argparse
import os
import shutil
import json

class Constants:
    RENAMING_ALLOWED_DIRECTORIES = ['flows', 'config', 'scripts']
    DEAULT_TEMPLATE_DIR_NAME = 'pyspark_template'

    DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME = 'employee_data_schema.json'
    DEAULT_TEMPLATE_CONFIG_FILE_NAME = 'pyspark_template.json'

    DEAULT_TEMPLATE_DATA_MIGRATION_FILE_NAME = 'pyspark_template_data_migration.py'
    DEAULT_TEMPLATE_PY_STARTER_FILE_NAME = 'pyspark_template.py'





class CommonLogging:
    @staticmethod
    def get_logger(log_level_str='INFO'):
        import logging
        try:
            level_num = logging.getLevelName(log_level_str.upper())
            if not isinstance(level_num, int):
                raise ValueError(f"Logging Level is not in predefined list: {str(level_num)}")

        except ValueError:
            level_num = logging.getLevelName('INFO')

        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=level_num,
                            datefmt='%y/%m/%d %H:%M:%S')

        return logging.getLogger()


logging = CommonLogging.get_logger()

class ProjectStructureGenerator:
    @staticmethod
    def _remove_file(file_path):
        # Check if the file exists before trying to remove it
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.debug(f"File {file_path} has been removed.")
        else:
            logging.debug(f"File {file_path} does not exist. File must be exist to remove!!!")
    @staticmethod
    def _rename_files(project_name):
        current_dir = os.getcwd()
        for dir in Constants.RENAMING_ALLOWED_DIRECTORIES:
            dir_path = os.path.join(current_dir,project_name,  dir)
            logging.debug(f"dir path {dir_path}")
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    if filename in [Constants.DEAULT_TEMPLATE_PY_STARTER_FILE_NAME, Constants.DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME,
                                            Constants.DEAULT_TEMPLATE_DATA_MIGRATION_FILE_NAME, Constants.DEAULT_TEMPLATE_CONFIG_FILE_NAME]:
                        # Determine new filename with the project_name preserved extension
                        _, ext = os.path.splitext(filename)
                        logging.debug(f"extention for {filename} is {ext}")
                        update_project_name = project_name.replace('-', '_')
                        new_filename = update_project_name + ext
                        # if filename == Constants.DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME:
                        #     new_filename = update_project_name + "_schema.json"
                        if filename == Constants.DEAULT_TEMPLATE_DATA_MIGRATION_FILE_NAME:
                            new_filename = update_project_name + "_data_migration.py"

                        original_file_path = os.path.join(dir_path, filename)
                        new_file_path = os.path.join(dir_path, new_filename)

                        if os.path.exists(original_file_path):
                            logging.debug(f"Renaming {original_file_path} to {new_file_path}")
                            os.rename(original_file_path, new_file_path)
                            logging.debug(f"Renamed {original_file_path} to {new_file_path}")
                        else:
                            logging.error(f"File {original_file_path} does not exist. Unable to rename a file!!!")

    @staticmethod
    def copy_and_rename_template(project_name, is_data_migration: bool= False):
        # Define paths
        template_dir = os.path.join(os.path.dirname(__file__), Constants.DEAULT_TEMPLATE_DIR_NAME)
        current_dir = os.getcwd()
        logging.info("current_dir: {}".format(current_dir))
        # Copy template directory to current directory
        try:
            shutil.copytree(template_dir, os.path.join(current_dir, project_name))
            logging.debug(f"Copying template directory from {template_dir} to {os.path.join(current_dir, project_name)}")
             # Log creation of first-level directories
            destination_dir = os.path.join(current_dir, project_name)
            for dirpath, _, _ in os.walk(destination_dir):
                if dirpath == destination_dir:
                    continue
                logging.info(f"Creating directory: {os.path.relpath(dirpath, destination_dir)}")

        except FileExistsError:
            logging.error(f"Error: Directory '{project_name}' already exists. Aborting.")
            return
        except Exception as e:
                raise Exception(f"Error occurred while copying template: {str(e)}")
        
        # List of directories where renaming is allowed
        if is_data_migration:
            # get the default template  script
            py_main_file_path = os.path.join(current_dir,project_name,  "scripts", Constants.DEAULT_TEMPLATE_PY_STARTER_FILE_NAME)
            # schema_file_path = os.path.join(current_dir,project_name,  "config", Constants.DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME)

            ProjectStructureGenerator._remove_file(file_path=py_main_file_path)
            # ProjectStructureGenerator._remove_file(file_path=schema_file_path)
        else:
            py_main_file_path = os.path.join(current_dir,project_name,  "scripts", Constants.DEAULT_TEMPLATE_DATA_MIGRATION_FILE_NAME)
            ProjectStructureGenerator._remove_file(file_path=py_main_file_path)

        ProjectStructureGenerator._rename_files(project_name=project_name)

    @staticmethod
    def update_template_script(project_name, is_data_migration: bool = False):
        """
        Updates the project-specific script file by replacing placeholder paths with the actual project path.

        This method modifies a script file within the project's `scripts` directory. If the script is found,
        it replaces occurrences of a placeholder path with the project-specific path.

        Parameters:
        -----------
        project_name : str
            The name of the project. This name is used to locate and update the script file.
        is_data_migration : bool, optional
            If True, updates the data migration script for the project. Default is False.

        Returns:
        --------
        None

        Raises:
        -------
        None
        """
        import fileinput
        import sys

        # Determine the script file name based on the project name and data migration flag
        file_name = f"{project_name}_data_migration.py" if is_data_migration else f"{project_name}.py"
        file_name = file_name.replace('-', '_')

        # Construct the full path to the script file
        pyspark_template_path = os.path.join(os.getcwd(), project_name, 'scripts', file_name)

        # Check if the script file exists
        if os.path.exists(pyspark_template_path):
            # Update the script file by replacing the placeholder path
            with fileinput.FileInput(pyspark_template_path, inplace=True) as file:
                for line in file:
                    # Replace the placeholder with the project-specific path
                    updated_line = line.replace('/workflows/pyspark_template/', f'/workflows/{project_name}/')
                    sys.stdout.write(updated_line)

            # Log the successful update
            logging.debug(f"Updated {file_name} with project-specific paths.")
        else:
            # Log an error if the script file does not exist
            logging.error(f"File {pyspark_template_path} does not exist!!!")
            raise Exception(f"File {pyspark_template_path} does not exist!!!\n")


    @staticmethod
    def read_config_file(project_name):
        """
        Reads a JSON configuration file for the given project and returns its content.

        This method constructs the file path based on the project name, reads the JSON content
        from the file, and returns the configuration data as a Python dictionary.

        Parameters:
        -----------
        project_name : str
            The name of the project for which the configuration file is to be read.

        Returns:
        --------
        tuple
            A tuple containing the following:
            - configurations (dict): The configuration data loaded from the JSON file.
            - full_config_file_path (str): The full path to the configuration file.

        Raises:
        -------
        Exception
            If any error occurs during the file reading process, an exception is raised with a detailed
            error message including the file path and the specific error encountered.
        """
        try:
            current_dir = os.getcwd()
            file_name = f"{project_name.replace('-', '_')}.json"
            full_config_file_path = os.path.join(current_dir, project_name, "config", file_name)
            
            with open(full_config_file_path, "r") as f:
                configurations = json.load(f)
            
            return configurations, full_config_file_path
        except Exception as e:
            raise Exception(f"Exception occurred while reading Config File: {full_config_file_path}, Error: {str(e)}")

    
    @staticmethod
    def update_template_config(configs, full_config_file_path, project_name, is_data_migration=False):
        airflow_dag_details = configs["airflow-dag-details"]
        airflow_dag_details["dag_id"] = project_name.replace('-', '_')

        airflow_task_details = configs.get("airflow-task-details", {})
        if airflow_task_details is not None:
            project_name_job = project_name.replace('_', '-')
            
            # Select the correct template based on is_data_migration flag
            template_key = "pyspark-template-migration" if is_data_migration else "pyspark-template"
            
            airflow_task_details[project_name_job] = airflow_task_details[template_key]
             # Delete the keys that are not needed based on is_data_migration flag
            keys_to_remove = [key for key in airflow_task_details.keys() if key != project_name_job]
            for key in keys_to_remove:
                del airflow_task_details[key]
            
            pyspark_job_main_file_s3_path = airflow_task_details[project_name_job]["spark_details"]["spark_kubernetes_args"]["pyspark_job_main_file_s3_path"]
            update_pyspark_job_main_file_s3_path = pyspark_job_main_file_s3_path.replace(Constants.DEAULT_TEMPLATE_DIR_NAME, project_name)
            
            if is_data_migration:

                update_pyspark_job_main_file_s3_path = update_pyspark_job_main_file_s3_path.replace((project_name + '_data_migration.py'), 
                                                                            (project_name.replace('-', '_') + '_data_migration.py'))
            else:
                update_pyspark_job_main_file_s3_path = update_pyspark_job_main_file_s3_path.replace((project_name + '.py'), 
                                                                            (project_name.replace('-', '_') + '.py'))
                # Update schema dir path
                # old_s3_schema_file_path = airflow_task_details[project_name_job]["spark_details"]["spark_job_args"].get("s3_schema_file_path")
                # if old_s3_schema_file_path:
                #     new_s3_schema_file_path = old_s3_schema_file_path.replace(Constants.DEAULT_TEMPLATE_DIR_NAME, project_name)
                #     new_s3_schema_file_path = new_s3_schema_file_path.replace(Constants.DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME,
                #                          (project_name.replace('-', '_') + "_schema.json"))
                #     airflow_task_details[project_name_job]["spark_details"]["spark_job_args"]["s3_schema_file_path"] = new_s3_schema_file_path

            airflow_task_details[project_name_job]["spark_details"]["spark_kubernetes_args"]["pyspark_job_main_file_s3_path"] = update_pyspark_job_main_file_s3_path

            # Add project_dir_name, task_name
            airflow_task_details[project_name_job]["spark_details"]["spark_job_args"]["project_dir_name"] = project_name
            
            configs["airflow-task-details"] = airflow_task_details
            configs["airflow-dag-details"] = airflow_dag_details
        
        return configs

    @staticmethod
    def write_to_config_file(configs, full_config_file_path):
        """
        Writes the provided configuration dictionary to a JSON file at the specified file path.

        This method serializes a Python dictionary (`configs`) into a JSON formatted string with
        an indentation level of 2 spaces and writes it to a file located at `full_config_file_path`.

        Parameters:
        -----------
        configs : dict
            The configuration data to be written to the file. This should be a valid Python dictionary
            that can be serialized into JSON format.

        full_config_file_path : str
            The full file path (including the file name) where the JSON configuration should be saved.
            If the file does not exist, it will be created. If the file already exists, its contents
            will be overwritten.

        Raises:
        -------
        Exception
            If any error occurs during the writing process, an exception will be raised with a detailed
            error message that includes the file path and the specific error encountered.

        Example Usage:
        --------------
        config_data = {
                "airflow-task-details": {
                    "pyspark-template": {
                    "spark_details": {
                        "spark_kubernetes_args": {...},
                        "spark_job_args": {...}
                    }
                    },
                    ...
                },
                "airflow-task-dependencies-details": {"task-auto-dependencies":{"trigger_order": "parallel"}},
                "airflow-dag-details": {"dag_id": "pyspark_template","dag_description": "Employee data ingestion project"}

            }
        config_file_path = "/path/to/config.json"
        
        ProjectStructureGenerator.write_to_config_file(config_data, config_file_path)

        """
        try:
            with open(full_config_file_path, "w") as f:
                configs_json = json.dumps(configs, indent=2)
                f.write(configs_json)
                logging.debug(f"Writing updates to config file completed.")
        except Exception as e:
            raise Exception( "Exception occurred while updating Config File: %s, Error:%s " % (full_config_file_path, str(e)))

