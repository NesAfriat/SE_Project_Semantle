import gensim.downloader as api

class ModelMap:
    _instance = None
    _model_map = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_model(self, model_name):
        if model_name in self._model_map:
            return self._model_map[model_name]
        else:
            if model_name== "local_word2vec":
               pass
            #TODO: Add intergraion with modelFcatory
            else:
               model = api.load(model_name)
               self._model_map[model_name] = model
            return model
