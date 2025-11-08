#!/usr/bin/env python3
"""
Code Map Generator - Creates a text file map of your codebase
Usage: 
  codemapper.exe
  codemapper.exe --src ./project --folders app,src --files config.php
  codemapper.exe --config myconfig
  codemapper.exe --src ./project --savetoconfig myconfig
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

def get_base_dir():
    """Get the directory where the executable or script is located"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

# Default text file extensions
DEFAULT_TEXT_EXTENSIONS = {
    '.php', '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss',
    '.json', '.xml', '.yml', '.yaml', '.md', '.txt', '.sql', '.sh', '.bash',
    '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rs', '.rb', '.vue',
    '.svelte', '.astro', '.env', '.gitignore', '.htaccess', '.conf', '.ini',
    '.sass', '.less', '.lock', '.toml', '.dockerfile', '.editorconfig'
}

# Common folders to skip by default
COMMON_SKIP_FOLDERS = {
    'node_modules', '.git', '.svn', '__pycache__', 'vendor', 
    '.idea', '.vscode', 'dist', 'build', '.next', '.cache',
    'coverage', '.pytest_cache', '.mypy_cache', 'venv', 'env',
    'codemapper'
}

class CodeMapGenerator:
    def __init__(self, config=None):
        self.config = config or {}
        self.text_extensions = set(self.config.get('text_extensions', DEFAULT_TEXT_EXTENSIONS))
        self.src_folders = self.config.get('src', ['.'])
        self.folders = self.config.get('folders', [])
        self.files = self.config.get('files', [])
        self.except_folders = set(self.config.get('except_folders', []))
        self.except_files = set(self.config.get('except_files', []))
        
        # Always exclude the script/exe itself
        is_frozen = getattr(sys, 'frozen', False)
        script_name = 'codemapper.exe' if is_frozen else 'codemapper.py'
        self.except_files.add(script_name)
        
        self.max_file_size = self.config.get('max_file_size_mb', 10) * 1024 * 1024
        
        # Set up default output folder
        base_dir = get_base_dir()
        default_output_folder = base_dir / "codemapper" / "output"
        default_output_folder.mkdir(parents=True, exist_ok=True)
        self.output = Path(self.config.get('output', default_output_folder / 'code_map.txt'))
        
        self.stats = {
            'text_files': 0,
            'binary_files': 0,
            'skipped_files': 0,
            'errors': 0,
            'total_size': 0
        }
    
    def normalize_path(self, path_str):
        """Normalize path for comparison"""
        return str(Path(path_str)).replace('\\', '/')
    
    def should_process_folder(self, folder_path, base_path):
        """Determine if folder should be processed"""
        rel_path = Path(folder_path).relative_to(base_path)
        rel_str = self.normalize_path(rel_path)
        folder_name = rel_path.name
        parts = rel_path.parts
        
        # Always skip the codemapper folder
        if "codemapper" in parts or "codemapper/" in rel_str:
            return False
        
        # Check if any part is in except_folders
        if any(rel_str.startswith(self.normalize_path(f)) for f in self.except_folders):
            return False
        
        # Check common skip patterns
        if any(skip in parts for skip in COMMON_SKIP_FOLDERS):
            if not self.folders:
                return False
            return any(rel_str.startswith(self.normalize_path(f)) for f in self.folders)
        
        # If folders list is specified, only process those
        if self.folders:
            return any(
                rel_str.startswith(self.normalize_path(f)) or 
                rel_str == self.normalize_path(f) or
                folder_name in self.folders
                for f in self.folders
            )
        
        return True
    
    def should_process_file(self, file_path, base_path):
        """Determine if file should be processed"""
        rel_path = Path(file_path).relative_to(base_path)
        rel_str = self.normalize_path(rel_path)
        filename = file_path.name
        
        # Always skip files inside codemapper/
        if "codemapper/" in rel_str or "codemapper\\" in str(rel_path):
            return False
        
        # Check except_files
        if filename in self.except_files or rel_str in self.except_files:
            return False
        
        # If files list is specified, only process those
        if self.files:
            return filename in self.files or rel_str in self.files
        
        # Check file size
        try:
            if file_path.stat().st_size > self.max_file_size:
                return False
        except:
            pass
        
        return True
    
    def is_text_file(self, file_path):
        """Check if file should have its content included"""
        ext = Path(file_path).suffix.lower()
        return ext in self.text_extensions
    
    def read_file_safely(self, file_path):
        """Try to read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                self.stats['errors'] += 1
                return f"[Error: {str(e)}]"
        except Exception as e:
            self.stats['errors'] += 1
            return f"[Error: {str(e)}]"
    
    def generate_map(self):
        """Generate the code map"""
        base_dir = get_base_dir()
        default_output_folder = base_dir / "codemapper" / "output"
        default_output_folder.mkdir(parents=True, exist_ok=True)
        
        # Ask if user wants timestamp
        timestamp = datetime.now().strftime("%m%d%y-%H%M")
        use_timestamp = input(f"Include timestamp in file name? (y/n) [{timestamp}]: ").strip().lower()
        if use_timestamp in ('y', 'yes', ''):
            filename = f"code_map_{timestamp}.txt"
        else:
            filename = "code_map.txt"
        
        # Set output path
        self.output = Path(self.config.get('output', default_output_folder / filename))
        self.output.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\nCode Map Generator")
        print(f"{'=' * 70}")
        
        with open(self.output, 'w', encoding='utf-8') as out:
            out.write(f"MAP: Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Process each source folder
            for src in self.src_folders:
                src_path = Path(src).resolve()
                
                if not src_path.exists():
                    print(f"⚠ Warning: Source folder not found: {src}")
                    continue
                
                if not src_path.is_dir():
                    print(f"⚠ Warning: Not a directory: {src}")
                    continue
                
                print(f"\n📁 Scanning: {src_path}")
                print(f"{'-' * 70}")
                
                # Walk through files
                for root, dirs, files in os.walk(src_path):
                    dirs[:] = [d for d in dirs if self.should_process_folder(Path(root) / d, src_path)]
                    
                    if not self.should_process_folder(root, src_path):
                        continue
                    
                    # Process files
                    for file in sorted(files):
                        file_path = Path(root) / file
                        rel_path = file_path.relative_to(src_path)
                        display_path = self.normalize_path(rel_path)
                        
                        if not self.should_process_file(file_path, src_path):
                            self.stats['skipped_files'] += 1
                            continue
                        
                        # Track file size
                        try:
                            file_size = file_path.stat().st_size
                            self.stats['total_size'] += file_size
                        except:
                            file_size = 0
                        
                        if self.is_text_file(file_path):
                            out.write(f"--{display_path}\n")
                            content = self.read_file_safely(file_path)
                            out.write(content)
                            if not content.endswith('\n'):
                                out.write('\n')
                            out.write("----\n")
                            self.stats['text_files'] += 1
                            print(f"  ✓ {display_path}")
                        else:
                            out.write(f"--{display_path}\n")
                            self.stats['binary_files'] += 1
                            print(f"  ◆ {display_path}")
            
            # Summary
            out.write(f"--SUMMARY\n")
            out.write(f"Text:{self.stats['text_files']} Binary:{self.stats['binary_files']} Skipped:{self.stats['skipped_files']}\n")
        
        # Final stats
        print(f"\n{'=' * 70}")
        print(f"✓ Map generated: {self.output}")
        print(f"  Text files: {self.stats['text_files']}")
        print(f"  Binary files: {self.stats['binary_files']}")
        print(f"  Skipped: {self.stats['skipped_files']}")
        print(f"  Size: {self.stats['total_size'] / (1024*1024):.2f} MB")
        
        # Prompt to open
        try:
            while True:
                choice = input("\nOpen output? [file/folder/none]: ").strip().lower()
                if choice == 'file':
                    print(f"Opening file: {self.output}")
                    os.startfile(self.output)
                    break
                elif choice == 'folder':
                    folder_path = self.output.parent.resolve()
                    print(f"Opening folder: {folder_path}")
                    os.startfile(folder_path)
                    break
                elif choice in ('none', ''):
                    break
                else:
                    print("Please type 'file', 'folder', or 'none'.")
        except Exception as e:
            print(f"⚠ Could not open: {e}")
        
        return True

def load_config(config_name):
    """Load configuration from config folder"""
    base_dir = get_base_dir()
    config_dir = base_dir / 'codemapper' / 'config'
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Try with and without .json extension
    config_paths = [
        config_dir / f"{config_name}.json",
        config_dir / config_name
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    print(f"📖 Loading config: {config_path}")
                    return json.load(f)
            except Exception as e:
                print(f"⚠ Error loading config: {e}")
                sys.exit(1)
    
    return None

def check_default_config():
    """Check if default config exists and return it"""
    base_dir = get_base_dir()
    config_dir = base_dir / 'codemapper' / 'config'
    default_config_path = config_dir / 'default.json'
    
    if default_config_path.exists():
        try:
            with open(default_config_path, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def save_config(args, config_name=None):
    """Save current arguments as config"""
    base_dir = get_base_dir()
    config_dir = base_dir / 'codemapper' / 'config'
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Use provided name or default
    if config_name is None or config_name == '':
        config_name = 'default'
    
    config_path = config_dir / f"{config_name}.json"
    
    # Build config from args
    config = {}
    
    if args.src:
        config['src'] = args.src if isinstance(args.src, list) else [args.src]
    else:
        config['src'] = ['.']
    
    if args.folders:
        config['folders'] = args.folders.split(',') if isinstance(args.folders, str) else args.folders
    
    if args.files:
        config['files'] = args.files.split(',') if isinstance(args.files, str) else args.files
    
    if args.except_folders:
        config['except_folders'] = args.except_folders.split(',') if isinstance(args.except_folders, str) else args.except_folders
    
    if args.except_files:
        config['except_files'] = args.except_files.split(',') if isinstance(args.except_files, str) else args.except_files
    
    if args.output:
        config['output'] = args.output
    
    if args.extensions:
        config['text_extensions'] = args.extensions.split(',')
    
    # Save
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"💾 Config saved: {config_path}")
    return config

def main():
    parser = argparse.ArgumentParser(
        description='Generate a text map of your codebase for AI context',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory (or use default config if exists)
  codemapper.exe
  
  # Scan specific source folders
  codemapper.exe --src ./project --src ./another
  
  # Only scan specific folders within source
  codemapper.exe --folders app,database,config
  
  # Only include specific files
  codemapper.exe --files config.php,routes.php
  
  # Exclude folders or files
  codemapper.exe --except-folders tests,logs --except-files .env
  
  # Custom output
  codemapper.exe --output ./maps/project.txt
  
  # Save command as config (creates default.json)
  codemapper.exe --src ./app --folders models,controllers --savetoconfig
  
  # Save command as named config
  codemapper.exe --src ./app --folders models,controllers --savetoconfig myapp
  
  # Load from named config
  codemapper.exe --config myapp
  
  # Load from default config (automatically used if no args provided)
  codemapper.exe
        """
    )
    
    parser.add_argument('--src', action='append', help='Source folder(s) to scan (default: ./)')
    parser.add_argument('--folders', help='Comma-separated list of folders to include')
    parser.add_argument('--files', help='Comma-separated list of specific files to include')
    parser.add_argument('--except-folders', help='Comma-separated list of folders to exclude')
    parser.add_argument('--except-files', help='Comma-separated list of files to exclude')
    parser.add_argument('--output', '-o', help='Output file path (default: code_map.txt)')
    parser.add_argument('--extensions', help='Comma-separated list of text file extensions')
    parser.add_argument('--config', help='Load configuration from config folder')
    parser.add_argument('--savetoconfig', nargs='?', const='default', help='Save current command as config')
    
    args = parser.parse_args()
    
    # If savetoconfig, save and exit
    if args.savetoconfig is not None:
        config = save_config(args, args.savetoconfig)
        print(f"✓ Configuration saved as '{args.savetoconfig}'")
        if args.savetoconfig == 'default':
            print(f"\n💡 This is now your default config!")
            print(f"   Just run 'codemapper.exe' with no arguments to use it.")
        else:
            print(f"\nTo use: codemapper.exe --config {args.savetoconfig}")
        sys.exit(0)
    
    # Determine if any arguments were provided (excluding program name)
    has_args = len(sys.argv) > 1
    
    # Load from config or build from args
    if args.config:
        # Explicitly load named config
        config = load_config(args.config)
        if config is None:
            print(f"⚠ Config not found: {args.config}")
            sys.exit(1)
    elif not has_args:
        # No arguments provided - check for default config
        default_config = check_default_config()
        if default_config:
            print("📖 Using default config (codemapper/config/default.json)")
            print("💡 To ignore default config, use any flag (e.g., --src .)\n")
            config = default_config
        else:
            # No default config exists
            print("⚠ No default configuration found (codemapper/config/default.json)")
            choice = input("Do you want to scan the entire codebase with default settings? (y/n): ").strip().lower()
            if choice in ('y', 'yes'):
                config = {'src': ['.'], 'folders': [], 'files': []}
                print("Scanning entire codebase...")
                print("💡 Tip: You can save this command as default for next time:")
                print("    codemapper.exe --savetoconfig")
            else:
                print("Aborting. Use --src or --savetoconfig to create a config first.")
                sys.exit(0)

    else:
        # Arguments provided - build config from args
        config = {}
        
        if args.src:
            config['src'] = args.src
        else:
            config['src'] = ['.']
        
        if args.folders:
            config['folders'] = args.folders.split(',')
        
        if args.files:
            config['files'] = args.files.split(',')
        
        if args.except_folders:
            config['except_folders'] = args.except_folders.split(',')
        
        if args.except_files:
            config['except_files'] = args.except_files.split(',')
        
        if args.output:
            config['output'] = args.output
        
        if args.extensions:
            config['text_extensions'] = args.extensions.split(',')
    
    # Generate the map
    generator = CodeMapGenerator(config)
    success = generator.generate_map()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()