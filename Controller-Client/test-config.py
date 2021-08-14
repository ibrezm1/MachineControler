import yaml

with open('config.yaml', 'r') as f:
     doc = yaml.safe_load(f)

print([tuple(x['region']) for x in doc['monitor']['points']])
