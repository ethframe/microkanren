class SingledispatchCache(dict):
    def __init__(self):
        super().__init__()
        self.exact = {}
        self.mro = {}
        self.mro_cache = {}

    def add(self, key, fn):
        self.mro[key] = fn
        self.mro_cache.clear()
        self.clear()

    def add_exact(self, key, fn):
        self.exact[key] = fn
        self.clear()

    def __missing__(self, key):
        if key in self.exact:
            fn = self[key] = self.exact[key]
            return fn
        for parent in key.__mro__:
            if parent in self.mro_cache:
                fn = self[key] = self.mro_cache[parent]
                self.mro_cache[key] = fn
                return fn
            if parent in self.mro:
                fn = self[key] = self.mro[parent]
                self.mro_cache[key] = self.mro_cache[parent] = fn
                return fn
        self[key] = None
