"""
Convert LDIF files to JSON format with optional hierarchical nesting.

This script parses LDIF input (from file or stdin) and converts it to JSON output,
with options for formatting and hierarchical nesting.
"""

import argparse
import json
import sys
from collections import defaultdict


def parse_ldif(input_data):
    """Parse LDIF data into a list of dictionaries.
    
    Args:
        input_data: A file-like object containing LDIF data.
        
    Returns:
        list: A list of dictionaries representing LDIF entries.
              Multivalued attributes are converted to arrays.
    """
    entries = []
    current_entry = defaultdict(list)
    
    for line in input_data:
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
            
        # Detect new entry start
        if (line.startswith('dn:') or line.startswith('dn::')) and current_entry:
            entries.append({k: v[0] if len(v) == 1 else v 
                          for k, v in current_entry.items()})
            current_entry = defaultdict(list)
            
        # Parse attribute: value pairs
        if ': ' in line:
            attr, value = line.split(': ', 1)
            current_entry[attr].append(value)
        elif ':: ' in line:  # Handle base64 encoded values
            attr, value = line.split(':: ', 1)
            current_entry[attr].append(value)
    
    # Add the last entry if exists
    if current_entry:
        entries.append({k: v[0] if len(v) == 1 else v 
                      for k, v in current_entry.items()})
    
    return entries


def nest_entries(entries, parent_attribute='subEntries'):
    """Nest LDIF entries hierarchically based on DN structure.
    
    Args:
        entries: List of LDIF entries as dictionaries.
        parent_attribute: Attribute name to use for nested entries.
        
    Returns:
        list: Root entries with nested children in parent_attribute.
    """
    entries_by_dn = {entry['dn']: entry for entry in entries if 'dn' in entry}
    sorted_dns = sorted(entries_by_dn.keys(), 
                       key=lambda x: len(x.split(',')), 
                       reverse=True)
    
    for dn in sorted_dns:
        entry = entries_by_dn[dn]
        parent_dn = ','.join(dn.split(',')[1:])  # Remove first RDN
        
        if parent_dn in entries_by_dn:
            parent_entry = entries_by_dn[parent_dn]
            if parent_attribute not in parent_entry:
                parent_entry[parent_attribute] = []
            parent_entry[parent_attribute].append(entry)
    
    # Return only root entries (those that aren't children)
    return [entry for dn, entry in entries_by_dn.items() 
            if not any(dn.endswith(','+parent) 
                     for parent in entries_by_dn.keys() 
                     if parent != dn)]


def main():
    """Main function to handle command line interface and processing."""
    parser = argparse.ArgumentParser(
        description='Convert LDIF files to JSON format with optional nesting',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input/output file arguments
    parser.add_argument(
        'input_file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='LDIF input file (use - for stdin)'
    )
    parser.add_argument(
        '-o', '--output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output JSON file (default: stdout)'
    )
    
    # Processing options
    parser.add_argument(
        '-i', '--indent',
        type=int,
        default=2,
        help='Indentation level for JSON output'
    )
    parser.add_argument(
        '-n', '--nest',
        metavar='ATTR',
        nargs='?',
        const='subEntries',
        default=None,
        help='Enable hierarchical nesting using specified attribute '
             '(default: "subEntries" when flag used without value)'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse LDIF input
        entries = parse_ldif(args.input_file)
        
        # Apply nesting if requested
        if args.nest is not None:
            entries = nest_entries(entries, args.nest)
        
        # Write JSON output
        json.dump(entries, args.output, indent=args.indent, ensure_ascii=False)
        args.output.write('\n')  # Add trailing newline
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
