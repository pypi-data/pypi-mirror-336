from .dataset import Dataset


def merge_dataset(dataset1_path: str, dataset2_path: str, output_path: str):
    dataset1 = Dataset(dataset1_path)
    dataset2 = Dataset(dataset2_path)
    merged_dataset = dataset1.merge(dataset2)
    merged_dataset.save(output_path)


def print_dataset_info(dataset_path: str):
    dataset = Dataset(dataset_path)
    dataset.print_info()
