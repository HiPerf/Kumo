from .. import generator


class LangGenerator(generator.Generator):
    def __init__(self, role, queues, messages, programs):
        super().__init__(role, queues, messages, programs)

