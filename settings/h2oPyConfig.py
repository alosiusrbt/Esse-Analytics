import yaml
import os

cfg = {}

with open("settings/dev.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)