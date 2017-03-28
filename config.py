import ujson

filename = 'config.json'
vars = {}
def init():
    try:
        file = open(filename, 'r')
    except OSError:
        print('No config.json file')
        return
    json = file.read()
    file.close()
    json = json.replace('\n', '').replace('\t', '')
    json = ' '.join(json.split()) #substitute multiple spaces with one
    try:
        global vars
        vars = ujson.loads(json)
        print('config init')
    except ValueError:
        print("File config.json doesn't contain proper JSON.")

def get(name):
    global vars
    parts = name.split('.')
    value = vars[parts[0]]
    for part in parts[1:]:
        value = value[part]
    return value

def exists(name):
    try:
        get(name)
        return True
    except KeyError:
        return False

def save():
    try:
        file = open(filename, 'w')
    except OSError:
        print('No config.json file')
        return
    global vars
    json = ujson.dumps(vars)
    file.write(json)
    file.close()

if len(vars) == 0:
    init()