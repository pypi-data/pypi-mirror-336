"""Command-line interface for interactively generating/acquiring metadata files."""

import re
import os

from pathlib import Path

from aind_metadata_service.client import AindMetadataServiceClient
from aind_data_schema.core.subject import Subject


class MetadataCLI:

    def __init__(self):
        pass

    def get_subject_id(self):
        """Prompt user for a subject ID and validate it."""
        while True:
            subject_id = input("Enter subject ID (6 digits): ").strip()
            if re.fullmatch(r"\d{6}", subject_id):
                return subject_id
            print("Invalid input. Please enter exactly six digits.")

    def get_acquisition_file(self):
        """Prompt user for an acquisition generator file."""
        while True:
            acquisition_file = input("Enter acquisition file [generate_acquisition.py]: ").strip()
            if not acquisition_file:
                acquisition_file = Path(__file__).parent / "generate_acquisition.py"

            # Check that the file exists
            if os.path.isfile(acquisition_file) and acquisition_file.suffix == ".py":
                return acquisition_file
            print("Invalid input. Please enter exactly a path to a file.")

    def gather(self):
        """Prompt user for data"""
        print('\n(Metadata CLI) - Gathering requirements from user...')
        self.subject_id = self.get_subject_id()
        self.acquistion_file = self.get_acquisition_file()

    def retrieve_subject(self, subject_id):
        """Placeholder function for calling the metadata client."""
        # Initialize client with the server domain
        # If you're at the Allen Institute, use one of these domains:
        client = AindMetadataServiceClient(domain="http://aind-metadata-service")  # production

        # Subject and procedures
        subject_data = client.get_subject(subject_id).json()

        subject = Subject.model_validate(subject_data['data'])
        subject.write_standard_file()

    def acquire(self):
        """Run CLI"""
        print('\n(Metadata CLI) - Running metadata-service and local files...')

        # Run the subject_id call
        try:
            self.retrieve_subject(self.subject_id)
        except Exception as e:
            print(f"Error retrieving subject: {e}")

        # Data description

        # Acquistion
        # call the acquisition file, passing the subject_id parameter
        try:
            os.system(f"python {self.acquistion_file} --subject-id {self.subject_id}")
        except Exception as e:
            print(f"Error running acquisition file: {e}")


if __name__ == "__main__":
    print('\n(Metadata CLI) - Initializing...')
    cli = MetadataCLI()
    cli.gather()
    cli.acquire()
    print('\n(Metadata CLI) - Done.')
