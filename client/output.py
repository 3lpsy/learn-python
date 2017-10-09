import json

class Output(object):
    def __init__(self, data, output_format):
        self.data = data
        self.format = output_format

    def _output_raw(self):
        print(self.data)

    def output(self):
        self._output_raw()

class DataOutput(Output):
    def __init__(self, data, output_format, columns=None, spacing=10):
        self.spacing = spacing
        self.columns = columns
        self.trimmers = {}
        super().__init__(data, output_format)
    def output(self):
        self._output_columns()
        if isinstance(self.data, list):
            for item in self.data:
                self._output_dict(item)
        elif isinstance(self.data, dict):
            self._output_dict(self.data)
        elif isinstance(self.data, str):
            try:
                loaded = json.loads(self.data)
                self.data = loaded
                self.output()
            except json.JSONDecodeError as ex:
                self._output_raw()
        else:
            self._output_raw()

    def _output_dict(self, item):
        tmp_item = []
        for key in self.columns:
            item_val = self._apply_trim(key, item[key])
            tmp_item.append(item_val)
        print(self.rowify(tmp_item))

    def _output_columns(self):
        print(self.rowify(self.columns))

    def rowify(self, vals):
        pattern = '{:<' + str(self.spacing) + '}'
        items_to_join = [pattern.format(val) for val in vals ]
        return "".join(items_to_join)

    def add_trimmer(self, key, trim_len=None):
        if not trim_len:
            trim_len = self.spacing
        self.trimmers[key] = trim_len

    def _apply_trim(self, key, val):
        trimmed_val = val
        if key in self.trimmers:
            trim_len = self.trimmers[key]
            if len(val) > trim_len:
                trimmed_val = val[:trim_len] + '..'
        return trimmed_val
