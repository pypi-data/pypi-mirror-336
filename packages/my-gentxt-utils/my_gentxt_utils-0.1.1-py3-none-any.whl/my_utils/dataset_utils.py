def load_data(data_path):
    with open(data_path, "r") as f:
        data = f.readlines()
    return data
