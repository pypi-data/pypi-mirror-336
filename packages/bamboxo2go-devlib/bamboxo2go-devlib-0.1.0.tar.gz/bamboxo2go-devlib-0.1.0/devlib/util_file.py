import glob
import os
import csv
from chardet import UniversalDetector


class FileUtil:
    @staticmethod
    def create_dir_if_not_exist(path):
        """Create directory if it doesn't exist"""
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def write_file_lines(file, lines):
        """Write lines to a file"""
        with open(file, mode='w', encoding='utf-8') as f:
            f.write("\n".join(lines))


    @staticmethod
    def append_file_lines(file, lines):
        """Append lines to a file"""
        with open(file, mode='a', encoding='utf-8-sig') as f:
            f.writelines("\n")
            f.writelines("\n".join(lines))

    @staticmethod
    def write_file(file, content):
        """Write content to a file"""
        with open(file, mode='a', encoding='utf-8-sig') as f:
            f.write(content)

    @staticmethod
    def read_file_lines(file, encoding='utf-8'):
        """Read lines from a file"""
        with open(file, mode='r', encoding=encoding) as f:
            return f.readlines()

    @staticmethod
    def read_file_lines_processed(file, encoding='utf-8-sig'):
        """Read and process lines from a file"""
        with open(file, mode='r', encoding=encoding) as f:
            return f.read().split("\n")

    @staticmethod
    def read_file(file):
        """Read entire file content"""
        with open(file, mode='r', encoding='utf-8-sig') as f:
            return f.read()

    @staticmethod
    def read_folder_files(folder_path, recursive=False):
        """Get list of files in a folder"""
        return glob.glob(folder_path, recursive=recursive)

    @staticmethod
    def detect_file_charset(path):
        """Detect file charset"""
        detector = UniversalDetector()
        detector.reset()
        with open(path, 'rb') as file:  # Use 'with' to ensure the file is properly closed
            for line in file:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        return detector.result

    @staticmethod
    def list_files(directory, recursive=True):
        """List all files in directory"""
        return [str(x) for x in glob.glob(directory, recursive=recursive)]

    @staticmethod
    def read_csv(file_path, delimiter=','):
        """Read CSV file and return as list of dictionaries"""
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            return list(reader)

    @staticmethod
    def write_csv(file_path, target, headers=None, delimiter=','):
        """Write list of dictionaries to CSV file"""
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = headers if headers else target[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for row in target:
                writer.writerow(row)
