import pandas as pd

def get_zones():
    path:str = "contents/taxi_zone_lookup.csv"
    data = pd.read_csv(path)
    data = data.drop(columns=["Borough", "service_zone"])
    data_dict = data.to_dict()

    l1 = list(data_dict["LocationID"].values())
    l2 = list(data_dict["Zone"].values())

    result = {}

    for i in range(len(l1)):
        k = l1[i]
        v = l2[i]
        result[k] = v

    return result

if __name__ == '__main__':
    print(get_zones())