import pandas as pd
import os
import chardet


class TestData:
    def __init__(self, data_path):
        self.data_path = data_path
        with open(data_path, 'rb') as f:
            tmp = chardet.detect(f.read(2))
        self.encoding = tmp['encoding']
        self.signal, self.file_name, self.unit, self.timeline = self.open_file_title(self.encoding)

    def open_csv_data(self, item_list):
        data_list = [i + 3 for i in item_list]
        data = pd.read_csv(self.data_path, skiprows=[0, 1, 2, 3, 4, 6, 7], header=0,
                           delimiter=',', encoding=self.encoding, usecols=data_list)
        name = [self.signal[i] for i in item_list]
        unit = [self.unit[i] for i in item_list]

        return name, unit, data

    def open_file_title(self, encoding):

        df = pd.read_csv(self.data_path, skiprows=5, header=0, nrows=3,
                         delimiter=',', encoding=encoding,
                         usecols=lambda title: title not in ["Time", "Time.1", "Time.2"])
        unit = df.iloc[0]
        prop = df.iloc[1]
        file_path, full_file_name = os.path.split(self.data_path)
        file_name, x = os.path.splitext(full_file_name)
        date_series = pd.read_csv(self.data_path, skiprows=[0, 1, 2, 3, 4, 6, 7], header=0,
                                  delimiter=',', encoding=encoding, usecols=["Time"], dtype={"Time": str}).squeeze(
            "columns")
        time_series = pd.read_csv(self.data_path, skiprows=[0, 1, 2, 3, 4, 6, 7], header=0,
                                  delimiter=',', encoding=encoding, usecols=["Time.1"],
                                  dtype={"Time.1": str}).squeeze("columns")
        millisecond_series = pd.read_csv(self.data_path, skiprows=[0, 1, 2, 3, 4, 6, 7], header=0,
                                         delimiter=',', encoding=encoding, usecols=["Time.2"],
                                         dtype={"Time.2": float}).squeeze("columns")
        microsecond_series_int = millisecond_series.mul(1000).astype("int")
        microsecond_series = microsecond_series_int.apply(lambda num: str(num).zfill(6))
        timeline_str = date_series.str.cat([time_series, microsecond_series], join="outer", sep=",")
        try:
            timeline = pd.to_datetime(timeline_str, format="%m/%d/%Y,%I:%M:%S %p,%f")
        except ValueError:
            try:
                timeline = pd.to_datetime(timeline_str, format="%Y/%m/%d,%H:%M:%S,%f")
            except ValueError as e:
                raise e
        timeline_numpy = timeline.to_numpy()

        return df.columns.values.tolist(), file_name, unit, timeline_numpy
