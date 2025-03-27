import json
from ..handle import Handle


class BaseTool:
    handleCount = 1

    # Is the tool attached to a chart?
    chart = None

    def __init__(self, data=None):
        if data is None:
            data = {"id": None, "handles": []}

        self.data = data

    def get_id(self) -> str:
        if 'id' not in self.data:
            return None

        return self.data['id']

    def set_id(self, id):
        self.data['id'] = id

    def get_type(self) -> str:
        if hasattr(self, 'type'):
            return self.type

        return self.data['type']

    def get_option(self, key, default_value=""):
        if key not in self.data['options']:
            return default_value

        return json.loads(self.data['options'][key])

    def set_option(self, key, value):
        if 'options' not in self.data:
            self.data['options'] = {}

        self.data['options'][key] = json.dumps(value)

    def set_lock(self, locked: bool):
        self.set_option('locked', locked)

    def save_options(self):
        if self.chart is None:
            raise Exception("Tool is not attached to a chart")

        tpro = self.chart.tpro

        tpro.rest.post(f"tools/options/{self.get_id()}", {
            "options": self.data['options']
        })

        print(f"Saving options {self.data['options']}")

    def available_options(self) -> dict:
        return self.data['options'].keys()

    def set_handles(self, handles):
        if len(handles) != self.handleCount:
            raise Exception(f"Invalid handle count  for {self.get_type()}")

        if len(handles) == 0:
            return

        self.data['time'] = handles[0][0]
        self.data['price'] = handles[0][1]

        if len(handles) > 1:
            if 'handles' not in self.data:
                self.data['handles'] = []

            for handle in handles[1:]:
                self.data['handles'].append({
                    'time': handle[0],
                    'price': handle[1]
                })

    def get_handles(self) -> list:
        handles = []

        if 'time' in self.data and 'price' in self.data:
            handles.append(Handle(self.data['time'], self.data['price']))

        if 'handles' in self.data:
            for handle in self.data['handles']:
                handles.append(Handle(handle['time'], handle['price']))

        return handles
