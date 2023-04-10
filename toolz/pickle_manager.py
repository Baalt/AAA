import pickle


class PickleHandler:
    def read_data(self, path_to_file):
        with open(path_to_file, "rb") as f:
            data = pickle.load(f)
        return data

    def write_data(self, data: dict, path_to_file):
        with open(path_to_file, "wb") as f:
            pickle.dump(data, f)
