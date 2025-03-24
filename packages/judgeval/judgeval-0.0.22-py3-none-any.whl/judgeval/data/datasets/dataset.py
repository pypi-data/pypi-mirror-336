import ast
import csv
import datetime
import json
import os
import yaml
from dataclasses import dataclass, field
from typing import List, Union, Literal

from judgeval.data import Example
from judgeval.common.logger import debug, error, warning, info

@dataclass
class EvalDataset:
    examples: List[Example]
    _alias: Union[str, None] = field(default=None)
    _id: Union[str, None] = field(default=None)
    judgment_api_key: str = field(default="")
    organization_id: str = field(default="")
    def __init__(self, 
                 judgment_api_key: str = os.getenv("JUDGMENT_API_KEY"),  
                 organization_id: str = os.getenv("JUDGMENT_ORG_ID"),
                 examples: List[Example] = [],
                 ):
        debug(f"Initializing EvalDataset with {len(examples)} examples")
        if not judgment_api_key:
            warning("No judgment_api_key provided")
        self.examples = examples
        self._alias = None
        self._id = None
        self.judgment_api_key = judgment_api_key
        self.organization_id = organization_id

    def add_from_json(self, file_path: str) -> None:
        debug(f"Loading dataset from JSON file: {file_path}")
        """
        Adds examples from a JSON file.

        The format of the JSON file is expected to be a dictionary with one key: "examples". 
        The value of the key is a list of dictionaries, where each dictionary represents an example.

        The JSON file is expected to have the following format:
        {
        "examples": [
            {
                "input": "test input",
                "actual_output": "test output",
                "expected_output": "expected output",
                "context": [
                    "context1",
                    "context2"
                ],
                "retrieval_context": [
                    "retrieval1"
                ],
                "additional_metadata": {
                    "key": "value"
                },
                "tools_called": [
                    "tool1"
                ],
                "expected_tools": [
                    "tool1",
                    "tool2"
                ],
                "name": "test example",
                "example_id": null,
                "timestamp": "20241230_160117",
                "trace_id": "123"
            }
            ]
        }
        """
        try:
            with open(file_path, "r") as file:
                payload = json.load(file)
                examples = payload.get("examples", [])
        except FileNotFoundError:
            error(f"JSON file not found: {file_path}")
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except json.JSONDecodeError:
            error(f"Invalid JSON file: {file_path}")
            raise ValueError(f"The file {file_path} is not a valid JSON file.")

        info(f"Added {len(examples)} examples from JSON")
        new_examples = [Example(**e) for e in examples]
        for e in new_examples:
            self.add_example(e)
  
    def add_from_csv(
        self, 
        file_path: str,
        ) -> None:
        """
        Add Examples from a CSV file.
        """
        try:
            import pandas as pd
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Please install pandas to use this method. 'pip install pandas'"
            )
        
        # Pandas naturally reads numbers in data files as ints, not strings (can lead to unexpected behavior)
        df = pd.read_csv(file_path, dtype={'trace_id': str})
        """
        Expect the CSV to have headers

        "input", "actual_output", "expected_output", "context", \
        "retrieval_context", "additional_metadata", "tools_called", \
        "expected_tools", "name", "comments", "source_file", "example", \
        "trace_id"

        We want to collect the examples separately which can
        be determined by the "example" column. If the value is True, then it is an
        example

        We also assume that if there are multiple retrieval contexts or contexts, they are separated by semicolons.
        This can be adjusted using the `context_delimiter` and `retrieval_context_delimiter` parameters.
        """
        examples = []

        for _, row in df.iterrows():
            data = {
                "input": row["input"],
                "actual_output": row["actual_output"] if pd.notna(row["actual_output"]) else None,
                "expected_output": row["expected_output"] if pd.notna(row["expected_output"]) else None,
                "context": row["context"].split(";") if pd.notna(row["context"]) else [],
                "retrieval_context": row["retrieval_context"].split(";") if pd.notna(row["retrieval_context"]) else [],
                "additional_metadata": ast.literal_eval(row["additional_metadata"]) if pd.notna(row["additional_metadata"]) else dict(),
                "tools_called": row["tools_called"].split(";") if pd.notna(row["tools_called"]) else [],
                "expected_tools": row["expected_tools"].split(";") if pd.notna(row["expected_tools"]) else [],
                "trace_id": row["trace_id"] if pd.notna(row["trace_id"]) else None,
                "example_id": str(row["example_id"]) if pd.notna(row["example_id"]) else None
            }
            if row["example"]:
                data["name"] = row["name"] if pd.notna(row["name"]) else None
                # every Example has `input` and `actual_output` fields
                if data["input"] is not None and data["actual_output"] is not None:
                    e = Example(**data)
                    examples.append(e)
                else:
                    raise ValueError("Every example must have an 'input' and 'actual_output' field.")
           

        for e in examples:
            self.add_example(e)

    def add_from_yaml(self, file_path: str) -> None:
        debug(f"Loading dataset from YAML file: {file_path}")
        """
        Adds examples from a YAML file.

        The format of the YAML file is expected to be a dictionary with one key: "examples". 
        The value of the key is a list of dictionaries, where each dictionary represents an example.

        The YAML file is expected to have the following format:
        examples:
          - input: "test input"
            actual_output: "test output"
            expected_output: "expected output"
            context:
              - "context1"
              - "context2"
            retrieval_context:
              - "retrieval1"
            additional_metadata:
              key: "value"
            tools_called:
              - "tool1"
            expected_tools:
              - "tool1"
              - "tool2"
            name: "test example"
            example_id: null
            timestamp: "20241230_160117"
            trace_id: "123"
        """
        try:
            with open(file_path, "r") as file:
                payload = yaml.safe_load(file)
                if payload is None:
                    raise ValueError("The YAML file is empty.")
                examples = payload.get("examples", [])
        except FileNotFoundError:
            error(f"YAML file not found: {file_path}")
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except yaml.YAMLError:
            error(f"Invalid YAML file: {file_path}")
            raise ValueError(f"The file {file_path} is not a valid YAML file.")

        info(f"Added {len(examples)} examples from YAML")
        new_examples = [Example(**e) for e in examples]
        for e in new_examples:
            self.add_example(e)

    def add_example(self, e: Example) -> None:
        self.examples = self.examples + [e]
        # TODO if we need to add rank, then we need to do it here
    
    def save_as(self, file_type: Literal["json", "csv", "yaml"], dir_path: str, save_name: str = None) -> None:
        """
        Saves the dataset as a file. Save only the examples.

        Args:
            file_type (Literal["json", "csv"]): The file type to save the dataset as.
            dir_path (str): The directory path to save the file to.
            save_name (str, optional): The name of the file to save. Defaults to None.
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") if save_name is None else save_name
        complete_path = os.path.join(dir_path, f"{file_name}.{file_type}")
        if file_type == "json":
            with open(complete_path, "w") as file:
                json.dump(
                    {
                        "examples": [e.to_dict() for e in self.examples],
                    },
                    file,
                    indent=4,
                )
        elif file_type == "csv":
            with open(complete_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "input", "actual_output", "expected_output", "context", \
                    "retrieval_context", "additional_metadata", "tools_called", \
                    "expected_tools", "name", "comments", "source_file", "example", \
                    "trace_id"
                ])
                for e in self.examples:
                    writer.writerow(
                        [
                            e.input,
                            e.actual_output,
                            e.expected_output,
                            ";".join(e.context),
                            ";".join(e.retrieval_context),
                            e.additional_metadata,
                            ";".join(e.tools_called),
                            ";".join(e.expected_tools),
                            e.name,
                            None,  # Example does not have comments
                            None,  # Example does not have source file
                            True,  # Adding an Example
                            e.trace_id
                        ]
                    )
                
                
        elif file_type == "yaml":
            with open(complete_path, "w") as file:
                yaml_data = {
                    "examples": [
                        {
                            "input": e.input,
                            "actual_output": e.actual_output,
                            "expected_output": e.expected_output,
                            "context": e.context,
                            "retrieval_context": e.retrieval_context,
                            "additional_metadata": e.additional_metadata,
                            "tools_called": e.tools_called,
                            "expected_tools": e.expected_tools,
                            "name": e.name,
                            "comments": None,  # Example does not have comments
                            "source_file": None,  # Example does not have source file
                            "example": True,  # Adding an Example
                            "trace_id": e.trace_id
                        }
                        for e in self.examples
                    ],
                }
                yaml.dump(yaml_data, file, default_flow_style=False)
        else:
            ACCEPTABLE_FILE_TYPES = ["json", "csv", "yaml"]
            raise TypeError(f"Invalid file type: {file_type}. Please choose from {ACCEPTABLE_FILE_TYPES}")
        
    def __iter__(self):
        return iter(self.examples)
    
    def __len__(self):
        return len(self.examples)
    
    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"examples={self.examples}, "
            f"_alias={self._alias}, "
            f"_id={self._id}"
            f")"
        )