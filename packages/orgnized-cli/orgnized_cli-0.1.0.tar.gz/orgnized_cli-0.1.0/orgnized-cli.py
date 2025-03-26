#!/usr/bin/env python3
"""
Organized CLI: A sophisticated file organization tool for efficient file management.

This script categorizes and organizes files in a specified directory
by their file types, creating structured folder hierarchies with configurable options.
"""

import os
import sys
import shutil
import argparse
import time
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set


class FileOrganizerConfig:
    """Configuration class for file organization settings."""
    def __init__(self):
        self.prefix = "orgz"  # Prefix for organized folders
        self.skip_hidden = True  # Skip hidden files/directories
        self.dry_run = False  # Preview changes without actually making them
        self.verbose = False  # Show detailed output
        self.conflict_resolution = "rename"  # Options: rename, skip, overwrite


# File extension categories (can be extended or modified)
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.heic', '.raw'],
    'Documents': [
        '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', 
        '.ppt', '.pptx', '.md', '.tex', '.epub', '.mobi'
    ],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus'],
    'Video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
    'Code': [
        '.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', 
        '.rb', '.go', '.rs', '.swift', '.kt', '.sh', '.pl', '.lua', '.ts'
    ],
    'Data': ['.csv', '.json', '.xml', '.yaml', '.yml', '.sql', '.db', '.sqlite'],
    'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.apk'],
    'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
}


class Colors:
    """ANSI color codes for terminal output with additional styling options."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'


class FileOrganizer:
    """Main file organizer class with all business logic."""
    
    def __init__(self, config: FileOrganizerConfig = FileOrganizerConfig()):
        self.config = config
        self.stats = {
            'files_processed': 0,
            'files_moved': 0,
            'files_copied': 0,
            'files_skipped': 0,
            'folders_created': 0,
            'errors': 0,
            'start_time': 0,
            'end_time': 0
        }
        self.errors: List[Tuple[str, str]] = []
    
    def print_header(self, text: str) -> None:
        """Print a formatted header."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}╒══[{text}]{Colors.ENDC}")
    
    def print_error(self, text: str) -> None:
        """Print an error message."""
        print(f"{Colors.RED}{Colors.BOLD}✗ Error: {text}{Colors.ENDC}")
        self.stats['errors'] += 1
    
    def print_success(self, text: str) -> None:
        """Print a success message."""
        print(f"{Colors.GREEN}{Colors.BOLD}✓ {text}{Colors.ENDC}")
    
    def print_warning(self, text: str) -> None:
        """Print a warning message."""
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ {text}{Colors.ENDC}")
    
    def print_info(self, text: str) -> None:
        """Print an informational message."""
        print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")
    
    def print_verbose(self, text: str) -> None:
        """Print verbose output if enabled."""
        if self.config.verbose:
            print(f"{Colors.GRAY}{text}{Colors.ENDC}")
    
    def get_category(self, file_ext: str) -> str:
        """
        Determine the category of a file based on its extension.
        
        Args:
            file_ext (str): File extension to categorize.
        
        Returns:
            str: Category name or 'Other' if no match found.
        """
        file_ext = file_ext.lower()
        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                return category
        return 'Other'
    
    def analyze_directory(self, directory_path: str) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
        """
        Analyze the directory to categorize files by extension.
        
        Args:
            directory_path (str): Path to the directory to analyze.
        
        Returns:
            Tuple containing:
            - Dictionary mapping categories to lists of files
            - Dictionary of extension counts
        
        Raises:
            FileNotFoundError: If directory does not exist
            NotADirectoryError: If path is not a directory
            PermissionError: If directory cannot be accessed
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Not a directory: {directory_path}")
        
        files_by_category = defaultdict(list)
        extension_counts = defaultdict(int)
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories and hidden files if configured
            if os.path.isdir(file_path) or (self.config.skip_hidden and filename.startswith('.')):
                self.print_verbose(f"Skipping: {filename}")
                continue
            
            # Get file extension and category
            _, file_ext = os.path.splitext(filename)
            if not file_ext:  # Files without extension
                category = 'No Extension'
            else:
                category = self.get_category(file_ext)
                extension_counts[file_ext.lower()] += 1
            
            files_by_category[category].append(file_path)
            self.stats['files_processed'] += 1
        
        return files_by_category, extension_counts
    
    def create_category_folders(self, directory_path: str, categories: Set[str]) -> List[str]:
        """
        Create folders for each category in the directory.
        
        Args:
            directory_path (str): Base directory path
            categories (Set[str]): Set of category names
        
        Returns:
            List of created folder names
        """
        created_folders = []
        
        for category in categories:
            prefixed_category = f"{self.config.prefix}{category}"
            category_path = os.path.join(directory_path, prefixed_category)
            
            if self.config.dry_run:
                self.print_info(f"[Dry Run] Would create folder: {prefixed_category}")
                created_folders.append(prefixed_category)
                continue
            
            try:
                os.makedirs(category_path, exist_ok=False)
                created_folders.append(prefixed_category)
                self.stats['folders_created'] += 1
                self.print_verbose(f"Created folder: {prefixed_category}")
            except FileExistsError:
                self.print_verbose(f"Folder exists: {prefixed_category}")
            except OSError as e:
                self.print_error(f"Failed to create folder {prefixed_category}: {e}")
        
        return created_folders
    
    def handle_file_conflict(self, destination: str) -> Optional[str]:
        """
        Handle file naming conflicts based on configuration.
        
        Args:
            destination (str): Original destination path
        
        Returns:
            Optional[str]: New destination path or None if should skip
        """
        if not os.path.exists(destination):
            return destination
        
        if self.config.conflict_resolution == "skip":
            self.print_verbose(f"Skipping existing file: {os.path.basename(destination)}")
            return None
        elif self.config.conflict_resolution == "overwrite":
            self.print_warning(f"Overwriting existing file: {os.path.basename(destination)}")
            return destination
        else:  # rename (default)
            base, ext = os.path.splitext(destination)
            counter = 1
            while True:
                new_destination = f"{base}_{counter}{ext}"
                if not os.path.exists(new_destination):
                    self.print_verbose(f"Renaming to avoid conflict: {os.path.basename(new_destination)}")
                    return new_destination
                counter += 1
    
    def organize_files(
        self,
        directory_path: str,
        files_by_category: Dict[str, List[str]],
        delete_originals: bool = False
    ) -> None:
        """
        Move or copy files to their respective category folders.
        
        Args:
            directory_path (str): Base directory path
            files_by_category (Dict[str, List[str]]): Mapping of categories to file paths
            delete_originals (bool): Whether to move (True) or copy (False) files
        """
        action = "Moving" if delete_originals else "Copying"
        
        for category, files in files_by_category.items():
            prefixed_category = f"{self.config.prefix}{category}"
            category_path = os.path.join(directory_path, prefixed_category)
            
            for file_path in files:
                filename = os.path.basename(file_path)
                original_destination = os.path.join(category_path, filename)
                
                try:
                    destination = self.handle_file_conflict(original_destination)
                    if destination is None:  # Skip this file
                        self.stats['files_skipped'] += 1
                        continue
                    
                    if self.config.dry_run:
                        self.print_info(f"[Dry Run] {action} {filename} to {prefixed_category}/")
                        self.stats['files_moved' if delete_originals else 'files_copied'] += 1
                        continue
                    
                    self.print_verbose(f"{action} {filename} to {prefixed_category}/")
                    
                    # Ensure target directory exists (might have been created in dry run)
                    os.makedirs(category_path, exist_ok=True)
                    
                    if delete_originals:
                        shutil.move(file_path, destination)
                        self.stats['files_moved'] += 1
                    else:
                        shutil.copy2(file_path, destination)  # copy2 preserves metadata
                        self.stats['files_copied'] += 1
                
                except (PermissionError, OSError, shutil.Error) as e:
                    self.errors.append((file_path, str(e)))
                    self.print_error(f"Failed to process {filename}: {e}")
    
    def request_permission(self, directory_path: str, delete_mode: bool) -> bool:
        """
        Request user permission to organize files with clear information.
        
        Args:
            directory_path (str): Path being organized
            delete_mode (bool): Whether files will be moved (deleted from source)
        
        Returns:
            bool: True if user grants permission, False otherwise
        """
        self.print_header("Permission Request")
        print(f"This tool will organize files in: {Colors.BOLD}{directory_path}{Colors.ENDC}")
        
        if delete_mode:
            self.print_warning("⚠ Warning: Original files will be MOVED (not copied)")
        else:
            self.print_info("Files will be copied (originals will remain)")
        
        if self.config.dry_run:
            self.print_info("Dry run mode: No changes will actually be made")
        
        while True:
            response = input(f"\n{Colors.BOLD}Proceed with organization? (y/n): {Colors.ENDC}").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Please enter 'y' for yes or 'n' for no.")
    
    def display_file_stats(self, files_by_category: Dict[str, List[str]]) -> None:
        """Display statistics about files found in the directory."""
        self.print_header("File Analysis")
        
        if not files_by_category:
            self.print_warning("No files found to organize.")
            return
        
        print("Found file types:")
        for category, files in sorted(files_by_category.items()):
            if files:
                # Get unique extensions for this category
                extensions = sorted({os.path.splitext(f)[1].lower() for f in files})
                ext_list = ", ".join(f"*{ext}" for ext in extensions)
                print(f"  {Colors.BOLD}{category:<12}{Colors.ENDC} {ext_list:<30} {len(files):>4} files")
        print()

    def display_summary(self) -> None:
        """Display a summary of the organization operation."""
        self.print_header("Operation Summary")
        
        # Calculate time taken
        time_taken = self.stats['end_time'] - self.stats['start_time']
        
        print(f"{Colors.BOLD}Files processed:{Colors.ENDC}   {self.stats['files_processed']}")
        if self.stats['files_moved'] > 0:
            print(f"{Colors.BOLD}Files moved:{Colors.ENDC}      {self.stats['files_moved']}")
        if self.stats['files_copied'] > 0:
            print(f"{Colors.BOLD}Files copied:{Colors.ENDC}     {self.stats['files_copied']}")
        if self.stats['files_skipped'] > 0:
            print(f"{Colors.BOLD}Files skipped:{Colors.ENDC}    {self.stats['files_skipped']}")
        
        print(f"{Colors.BOLD}Folders created:{Colors.ENDC}  {self.stats['folders_created']}")
        print(f"{Colors.BOLD}Time taken:{Colors.ENDC}       {time_taken:.2f} seconds\n")
        
        if self.errors:
            self.print_header("Errors Encountered")
            print(f"There were {len(self.errors)} errors during processing:")
            for file_path, error in self.errors[:5]:  # Show first 5 errors
                print(f"  {Colors.RED}✗{Colors.ENDC} {os.path.basename(file_path)}: {error}")
            if len(self.errors) > 5:
                print(f"  {Colors.GRAY}(and {len(self.errors)-5} more errors){Colors.ENDC}")
        
        if self.stats['errors'] == 0 and not self.config.dry_run:
            self.print_success(" Organization completed successfully!\n")
        elif self.config.dry_run:
            self.print_info("Dry run completed - no changes were made")


def main() -> None:
    """Main entry point for the Organized CLI tool."""
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by their types.",
        epilog="Example: orgnized-cli ~/Downloads --delete --verbose"
    )
    parser.add_argument(
        "directory",
        help="Path to the directory to organize"
    )
    parser.add_argument(
        "--delete", 
        action="store_true",
        help="Move files instead of copying (delete originals)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without actually making them"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output of operations"
    )
    parser.add_argument(
        "--prefix",
        default="orgz",
        help="Prefix for organized folders (default: 'orgz')"
    )
    parser.add_argument(
        "--conflict",
        choices=["rename", "skip", "overwrite"],
        default="rename",
        help="How to handle file conflicts (default: rename)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize configuration
        config = FileOrganizerConfig()
        config.dry_run = args.dry_run
        config.verbose = args.verbose
        config.prefix = args.prefix
        config.conflict_resolution = args.conflict
        
        # Initialize organizer
        organizer = FileOrganizer(config)
        directory_path = os.path.abspath(args.directory)
        
        # Display header
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}=== Organized CLI ==={Colors.ENDC}")
        print(f"Directory: {directory_path}")
        print(f"GitHub: https://github.com/karvanpy/orgnized-cli")
        
        # Request permission
        if not organizer.request_permission(directory_path, args.delete):
            print("Operation cancelled by user.")
            return
        
        # Start timing
        organizer.stats['start_time'] = time.time()
        
        # Analyze directory
        try:
            files_by_category, _ = organizer.analyze_directory(directory_path)
            organizer.display_file_stats(files_by_category)
            
            if not files_by_category:
                return  # No files to organize
            
            # Create folders and organize files
            organizer.create_category_folders(directory_path, set(files_by_category.keys()))
            organizer.organize_files(directory_path, files_by_category, args.delete)
            
        except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
            organizer.print_error(str(e))
            return
        
        # Complete timing
        organizer.stats['end_time'] = time.time()
        
        # Display summary
        organizer.display_summary()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Operation cancelled by user.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}{Colors.BOLD}Unexpected error:{Colors.ENDC} {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
