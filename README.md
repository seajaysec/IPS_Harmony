
# IPS Harmony Tool

## Overview
The IPS Harmony Tool is designed to evaluate multiple IPS (International Patching System) patches to determine if they conflict with each other when applied to a single target ROM. If the patches are in harmony (i.e., they do not conflict), the tool will apply all the patches to the ROM in one operation, creating a new patched version of the ROM.

## Goal
The primary goal of this tool is to streamline the process of applying multiple IPS patches to a ROM file. It first checks for conflicts between patches to ensure that they do not overwrite the same section of the ROM with different data. If no conflicts are detected, it applies all patches to create a single, cohesively modified ROM.

## Prerequisites
- Python 3.x installed on your system.
- The IPS patch files and the target ROM file.

## Installation
Clone the repository or download the script directly from the GitHub page.

## Usage
To use the IPS Harmony Tool, follow these steps:

1. **Prepare Your Files**:
   - Place all your IPS patch files in a single directory.
   - Ensure you have the target ROM file that you wish to patch.

2. **Run the Tool**:
   - Use the following command to run the tool:
     \```bash
     python harmonips.py -d /path/to/ips_patches_directory -r /path/to/rom/file.rom
     \```
   - Replace `/path/to/ips_patches_directory` with the path to the directory containing your IPS files.
   - Replace `/path/to/rom/file.rom` with the path to your target ROM file.

3. **Review the Output**:
   - The tool will analyze the patches and report if any conflicts are detected.
   - If no conflicts are found, it will apply all the patches to the ROM file, saving the patched version as a new file with the current date and time appended to its filename.

## Example
\```bash
python harmonips.py -d ./patches -r ./roms/mygame.rom
\```

## Note
- Patching is non-destructive. (Patched roms are saved as new files.)
- The tool is designed for basic IPS patch formats and may not cover every edge case.

## Contributing
Contributions, issues, and feature requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
