#!/usr/bin/env python3
"""
Configuration validator for ZK Middleware
"""

import yaml
import sys
import os

REQUIRED_FIELDS = {
    'device': ['ip', 'port'],
    'school_api': ['base_url'],
    'printer': ['type'],
    'app': ['listen_host', 'listen_port']
}

def validate_config(config_path):
    """Validate configuration file"""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file {config_path} not found")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Failed to parse configuration file: {e}")
        return False
    
    # Check required sections
    for section, fields in REQUIRED_FIELDS.items():
        if section not in config:
            print(f"Error: Missing section '{section}' in configuration")
            return False
        
        section_config = config[section]
        for field in fields:
            if field not in section_config:
                print(f"Error: Missing field '{field}' in section '{section}'")
                return False
    
    # Validate printer configuration
    printer_config = config['printer']
    if printer_config['type'] == 'network':
        if 'network' not in printer_config:
            print("Error: Missing 'network' subsection for network printer")
            return False
        if 'host' not in printer_config['network']:
            print("Error: Missing 'host' field for network printer")
            return False
    
    print("Configuration validation passed!")
    return True

if __name__ == "__main__":
    config_path = "config.example.yml"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    success = validate_config(config_path)
    sys.exit(0 if success else 1)