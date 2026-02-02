import yaml
import os

def configLoad(configPath):
    # check if file exists
    if not os.path.exists(configPath):
        raise FileNotFoundError(f"Config file not found: {configPath}")

    with open(configPath, 'r') as file:
        configData = yaml.safe_load(file)

    return configData
