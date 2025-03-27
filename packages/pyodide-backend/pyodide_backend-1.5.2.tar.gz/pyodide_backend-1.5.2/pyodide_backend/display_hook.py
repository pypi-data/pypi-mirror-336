class DisplayHook:
    def __init__(self):
        self.result = []
        self.returns_result = True

    def __call__(self, value):
        if value is None or not self.returns_result:
            return

        result_repr = repr(value)
        if "\n" in result_repr:
            result_repr = "\n" + result_repr

        self.result.append(result_repr)

    def has_result(self):
        return len(self.result) > 0

    def fetch_result(self):
        return self.result.pop()
