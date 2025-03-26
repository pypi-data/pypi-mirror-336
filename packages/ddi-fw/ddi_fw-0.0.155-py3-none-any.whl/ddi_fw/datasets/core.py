import glob
from typing import Any, Dict, List, Optional, Type
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, computed_field
from ddi_fw.datasets.dataset_splitter import DatasetSplitter
from ddi_fw.datasets.feature_vector_generation import SimilarityMatrixGenerator, VectorGenerator
from ddi_fw.langchain.embeddings import PoolingStrategy
from ddi_fw.utils.utils import create_folder_if_not_exists


def stack(df_column):
    return np.stack(df_column.values)


def generate_vectors(df, columns):
    vectorGenerator = VectorGenerator(df)
    generated_vectors = vectorGenerator.generate_feature_vectors(
        columns)
    return generated_vectors


def generate_sim_matrices_new(df, generated_vectors, columns, key_column="id"):
    jaccard_sim_dict = {}
    sim_matrix_gen = SimilarityMatrixGenerator()

    for column in columns:
        # key = '2D_'+column
        key = column
        jaccard_sim_dict[column] = sim_matrix_gen.create_jaccard_similarity_matrices(
            generated_vectors[key])

    similarity_matrices = {}
    keys = df[key_column].to_list()
    new_columns = {}
    for idx in range(len(keys)):
        new_columns[idx] = keys[idx]
    for column in columns:
        new_df = pd.DataFrame.from_dict(jaccard_sim_dict[column])
        new_df = new_df.rename(index=new_columns, columns=new_columns)
        similarity_matrices[column] = new_df
    return similarity_matrices


class BaseDataset(BaseModel):
    dataset_name: str
    index_path: str
    dataset_splitter_type: Type[DatasetSplitter]
    class_column: str = 'class'
    dataframe: Optional[pd.DataFrame] = None
    X_train:	Optional[pd.DataFrame] = None
    X_test:	Optional[pd.DataFrame] = None
    y_train:	Optional[pd.Series] = None
    y_test:	Optional[pd.Series] = None
    train_indexes:	Optional[pd.Index] = None
    test_indexes:	Optional[pd.Index] = None
    train_idx_arr:	List|None = None
    val_idx_arr:	List|None = None
    # train_idx_arr:	Optional[List[np.ndarray]] = None
    # val_idx_arr:	Optional[List[np.ndarray]] = None
    columns: List[str] = []

    # feature_process: FeatureProcessor
    # similarity_matrix_service: SimilarityMatrixService

    class Config:
        arbitrary_types_allowed = True

    def produce_inputs(self):
        items = []
        if self.X_train is None or self.X_test is None:
            raise Exception("There is no data to produce inputs")
        y_train_label, y_test_label = stack(self.y_train), stack(self.y_test)

        for column in self.columns:
            train_data, test_data = stack(
                self.X_train[column]), stack(self.X_test[column])
            items.append([f'{column}', np.nan_to_num(train_data),
                          y_train_label, np.nan_to_num(test_data), y_test_label])

            # items.append([f'{column}_embedding', train_data,
            #             y_train_label, test_data, y_test_label])
        return items
    
    @computed_field
    @property
    def dataset_splitter(self) -> DatasetSplitter:
        return self.dataset_splitter_type()

    def set_dataframe(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    # @abstractmethod
    def prep(self):
        pass

    def load(self):
        if self.index_path is None:
            raise Exception(
                "There is no index path, please call split function")

        try:
            train_idx_all, test_idx_all, train_idx_arr, val_idx_arr = self.__get_indexes__(
                self.index_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Index files not found: {e.filename}")

        self.prep()

        if self.dataframe is None:
            raise Exception("There is no dataframe")

        train = self.dataframe[self.dataframe.index.isin(train_idx_all)]
        test = self.dataframe[self.dataframe.index.isin(test_idx_all)]

        self.X_train = train.drop(self.class_column, axis=1)
        self.y_train = train[self.class_column]
        self.X_test = test.drop(self.class_column, axis=1)
        self.y_test = test[self.class_column]

        self.train_indexes = self.X_train.index
        self.test_indexes = self.X_test.index
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr

        return self.X_train, self.X_test, self.y_train, self.y_test, self.X_train.index, self.X_test.index, train_idx_arr, val_idx_arr

    def __get_indexes__(self, path):
        train_index_path = path+'/train_indexes.txt'
        test_index_path = path+'/test_indexes.txt'
        train_fold_files = f'{path}/train_fold_*.txt'
        val_fold_files = f'{path}/validation_fold_*.txt'
        train_idx_arr = []
        val_idx_arr = []
        with open(train_index_path, 'r', encoding="utf8") as f:
            train_idx_all = [int(r) for r in f.readlines()]
        with open(test_index_path, 'r', encoding="utf8") as f:
            test_idx_all = [int(r) for r in f.readlines()]

        for filepath in glob.glob(train_fold_files):
            with open(filepath, 'r', encoding="utf8") as f:
                train_idx = [int(r) for r in f.readlines()]
                train_idx_arr.append(train_idx)
        for filepath in glob.glob(val_fold_files):
            with open(filepath, 'r', encoding="utf8") as f:
                val_idx = [int(r) for r in f.readlines()]
                val_idx_arr.append(val_idx)
        return train_idx_all, test_idx_all, train_idx_arr, val_idx_arr

    def __save_indexes__(self, path, filename, indexes):
        create_folder_if_not_exists(path)
        file_path = path + '/'+filename
        str_indexes = [str(index) for index in indexes]
        with open(file_path, 'w') as f:
            f.write('\n'.join(str_indexes))

    def split_dataset(self, save_indexes: bool = False):
        # TODO class type should be parametric

        save_path = self.index_path
        self.prep()

        if self.dataframe is None:
            raise Exception("There is no data")

        X = self.dataframe.drop(self.class_column, axis=1)
        y = self.dataframe[self.class_column]

        X_train, X_test, y_train, y_test, X_train.index, X_test.index, train_idx_arr, val_idx_arr = self.dataset_splitter.split(
            X=X, y=y)
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.train_indexes = X_train.index
        self.test_indexes = X_test.index
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr

        if save_indexes:
            # train_pairs = [row['id1'].join(',').row['id2'] for index, row in X_train.iterrows()]
            self.__save_indexes__(
                save_path, 'train_indexes.txt', self.train_indexes.values)
            self.__save_indexes__(
                save_path, 'test_indexes.txt',  self.test_indexes.values)

            for i, (train_idx, val_idx) in enumerate(zip(train_idx_arr, val_idx_arr)):
                self.__save_indexes__(
                    save_path, f'train_fold_{i}.txt', train_idx)
                self.__save_indexes__(
                    save_path, f'validation_fold_{i}.txt', val_idx)

        # return X_train, X_test, y_train, y_test, folds


class TextDatasetMixin(BaseDataset):
    embedding_size: Optional[int] = None 
    embedding_dict: Dict[str, Any] = Field(default_factory=dict, description="Dictionary for embeddings")
    embeddings_pooling_strategy: PoolingStrategy | None = None

    def process_text(self):
        pass


# class ImageDatasetMixin(BaseModel):
#     image_size: tuple[int, int] = Field(default=(224, 224))
#     augmentations: list[str] = Field(default_factory=list)

#     def process_image_data(self):
#         print(
#             f"Processing image data with size {self.image_size} and augmentations {self.augmentations}...")
