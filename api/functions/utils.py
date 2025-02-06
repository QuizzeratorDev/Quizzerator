from werkzeug.utils import secure_filename
import os, json
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path_parent = os.path.abspath(os.path.join(dir_path, os.pardir))
dir_save = dir_path_parent + os.sep + "saves" + os.sep
def save_json(json_file, filename):
    json_object = json.dumps(json_file)
    name = secure_filename(filename + ".json")
    with open(dir_save + name, 'w') as f:
        json.dump(json_object, f)

def load_json(filename):
    
    with open(dir_save + str(filename) + '.json') as f:
        d = json.load(f)
        return d