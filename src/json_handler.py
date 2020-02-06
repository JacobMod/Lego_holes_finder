import json


class JsonHandler:


    def load_json(self, input_file):
        with open(input_file) as f:
            data = json.load(f)

        data = self.change_values_to_int(data)

        return data


    #get names of images in input json
    def get_data_names(self, data):
        labels = []
        for j in data:
            labels.append(j)

        return labels


    #changes value for every key in dict for int
    def change_values_to_int(self, data):
        for i in data:
            for d in data[i]:
                for key in d:
                    d[key] = int(d[key])

        return data
    

    def write_json(self, file_path, labels, right_places):
        data = {}
        for i, l in enumerate(labels):
            data[l] = right_places[i]

        with open(file_path, 'w') as output_file:
            json.dump(data, output_file, indent = 4)





