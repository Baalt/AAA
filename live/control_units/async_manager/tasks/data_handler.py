import pickle


class SmartDataHandler:
    def read_data(self):
        with open("smart_data.pkl", "rb") as f:
            data = pickle.load(f)
        return data

    def write_data(self, data):
        with open("smart_data.pkl", "wb") as f:
            pickle.dump(data, f)