from typing import Any, Dict, List, Optional, Type, Union
from ddi_fw.datasets.dataset_splitter import DatasetSplitter
import numpy as np
import pandas as pd
import chromadb
from collections import defaultdict
from chromadb.api.types import IncludeEnum

from pydantic import BaseModel
from ddi_fw.datasets.core import TextDatasetMixin
from ddi_fw.ner.ner import CTakesNER
from ddi_fw.langchain.embeddings import PoolingStrategy
from ddi_fw.datasets import BaseDataset, DDIMDLDataset
from ddi_fw.langchain.embeddings import SumPoolingStrategy
import mlflow
from ddi_fw.ml import MultiModalRunner


class Pipeline(BaseModel):
    library: str = 'tensorflow'
    experiment_name: str
    experiment_description: str
    experiment_tags: Optional[Dict[str, Any]] = None
    artifact_location: Optional[str] = None
    tracking_uri: Optional[str] = None
    dataset_type: Type[BaseDataset]
    dataset_splitter_type: Type[DatasetSplitter] = DatasetSplitter
    columns: Optional[List[str]] = None
    embedding_dict: Optional[Dict[str, Any]] = None
    column_embedding_configs: Optional[Dict] = None
    vector_db_persist_directory: Optional[str] = None
    vector_db_collection_name: Optional[str] = None
    embedding_pooling_strategy_type: Type[PoolingStrategy] | None = None
    ner_data_file: Optional[str] = None
    ner_threshold: Optional[dict] = None
    combinations: Optional[List[str]] = None
    model: Optional[Any] = None
    multi_modal:  Optional[Any] = None
    use_mlflow: bool = True
    _items:List=[]
    _train_idx_arr:List|None=[]
    _val_idx_arr:List|None=[]
    
    @property
    def items(self) -> List:
        return self._items
    @property
    def train_idx_arr(self) -> List|None:
        return self._train_idx_arr
    @property
    def val_idx_arr(self) -> List|None:
        return self._val_idx_arr

    class Config:
        arbitrary_types_allowed = True

# class Pipeline:
#     def __init__(self,
#                  library='tensorflow',
#                  experiment_name=None,
#                  experiment_description=None,
#                  experiment_tags=None,
#                  artifact_location=None,
#                  tracking_uri=None,
#                  dataset_type: BaseDataset = None,
#                  columns=None,
#                  embedding_dict=None,
#                  column_embedding_configs=None,
#                  vector_db_persist_directory=None,
#                  vector_db_collection_name=None,
#                  embedding_pooling_strategy_type: PoolingStrategy = None,
#                  ner_data_file=None,
#                  ner_threshold=None,
#                  combinations=None,
#                  model=None,
#                  multi_modal = None ):
#         self.library = library
#         self.experiment_name = experiment_name
#         self.experiment_description = experiment_description
#         self.experiment_tags = experiment_tags
#         self.artifact_location = artifact_location
#         self.tracking_uri = tracking_uri
#         self.dataset_type = dataset_type
#         self.columns = columns
#         self.embedding_dict = embedding_dict
#         self.column_embedding_configs = column_embedding_configs
#         self.vector_db_persist_directory = vector_db_persist_directory
#         self.vector_db_collection_name = vector_db_collection_name
#         self.embedding_pooling_strategy_type = embedding_pooling_strategy_type
#         self.ner_data_file = ner_data_file
#         self.ner_threshold = ner_threshold
#         self.combinations = combinations
#         self.model = model
#         self.multi_modal = multi_modal

    def __create_or_update_embeddings__(self, embedding_dict, vector_db_persist_directory, vector_db_collection_name, column=None):
        """
        Fetch embeddings and metadata from a persistent Chroma vector database and update the provided embedding_dict.

        Args:
        - vector_db_persist_directory (str): The path to the directory where the Chroma vector database is stored.
        - vector_db_collection_name (str): The name of the collection to query.
        - embedding_dict (dict): The existing dictionary to update with embeddings.

        """
        if vector_db_persist_directory:
            # Initialize the Chroma client and get the collection
            vector_db = chromadb.PersistentClient(
                path=vector_db_persist_directory)
            collection = vector_db.get_collection(vector_db_collection_name)
            include = [IncludeEnum.embeddings, IncludeEnum.metadatas]
            dictionary: chromadb.GetResult
            # Fetch the embeddings and metadata
            if column == None:
                dictionary = collection.get(
                    include=include
                    # include=['embeddings', 'metadatas']
                )
                print(
                    f"Embeddings are calculated from {vector_db_collection_name}")
            else:
                dictionary = collection.get(
                    include=include,
                    # include=['embeddings', 'metadatas'],
                    where={
                        "type": {"$eq": f"{column}"}})
                print(
                    f"Embeddings of {column} are calculated from {vector_db_collection_name}")

            # Populate the embedding dictionary with embeddings from the vector database
            metadatas = dictionary["metadatas"]
            embeddings = dictionary["embeddings"]
            if metadatas is None or embeddings is None:
                raise ValueError(
                    "The collection does not contain embeddings or metadatas.")
            for metadata, embedding in zip(metadatas, embeddings):
                embedding_dict[metadata["type"]
                               ][metadata["id"]].append(embedding)

        else:
            raise ValueError(
                "Persistent directory for the vector DB is not specified.")

    def build(self):
        if self.embedding_pooling_strategy_type is not None and not isinstance(self.embedding_pooling_strategy_type, type):
            raise TypeError(
                "self.embedding_pooling_strategy_type must be a class, not an instance")
        if not isinstance(self.dataset_type, type):
            raise TypeError(
                "self.dataset_type must be a class, not an instance")

        # 'enzyme','target','pathway','smile','all_text','indication', 'description','mechanism_of_action','pharmacodynamics', 'tui', 'cui', 'entities'
        kwargs = {"columns": self.columns}
        if self.ner_threshold:
            for k, v in self.ner_threshold.items():
                kwargs[k] = v
        if self.embedding_dict == None:
            embedding_dict = defaultdict(lambda: defaultdict(list))
            # TODO find more effective solution

            if self.column_embedding_configs:
                for item in self.column_embedding_configs:
                    col = item["column"]
                    col_db_dir = item["vector_db_persist_directory"]
                    col_db_collection = item["vector_db_collection_name"]
                    self.__create_or_update_embeddings__(
                        embedding_dict, col_db_dir, col_db_collection, col)

            elif self.vector_db_persist_directory:
                self.__create_or_update_embeddings__(
                    embedding_dict, self.vector_db_persist_directory, self.vector_db_collection_name)

            else:
                print(
                    f"There is no configuration of Embeddings")

        else:
            embedding_dict = self.embedding_dict
            # TODO make generic
            # embedding_size = list(embedding_dict['all_text'].values())[
            #     0][0].shape

        # self.ner_df = CTakesNER(df=None).load(
        #     filename=self.ner_data_file) if self.ner_data_file else None

        dataset_splitter = self.dataset_splitter_type()
        
        if issubclass(self.dataset_type, TextDatasetMixin):
            key, value = next(iter(embedding_dict.items()))
            embedding_size = value[next(iter(value))][0].shape[0]
            pooling_strategy = self.embedding_pooling_strategy_type() if self.embedding_pooling_strategy_type  else None

            dataset = self.dataset_type(
                embedding_dict=embedding_dict,
                embedding_size=embedding_size,
                embeddings_pooling_strategy=pooling_strategy,
                dataset_splitter = dataset_splitter,
                **kwargs)
        else:
            dataset = self.dataset_type(**kwargs)

        X_train, X_test, y_train, y_test, X_train.index, X_test.index, train_idx_arr, val_idx_arr = dataset.load()

        dataframe = dataset.dataframe

        if dataframe is None:  # if the dataframe is None, it means that the dataset is not loaded
            raise ValueError("The dataset is not loaded")

        # dataframe.dropna()
        X_train = dataset.X_train
        X_test = dataset.X_test
        y_train = dataset.y_train
        y_test = dataset.y_test
        self._train_idx_arr = dataset.train_idx_arr
        self._val_idx_arr = dataset.val_idx_arr
        # Logic to set up the experiment
        # column name, train data, train label, test data, test label
        self._items = dataset.produce_inputs()

        # unique_classes = pd.unique(dataframe[dataset.class_column])
        # event_num = len(unique_classes)
        # droprate = 0.3
        # vector_size = self.dataset.drugs_df.shape[0]

        print("Building the experiment with the following settings:")
        print(
            f"Name: {self.experiment_name}, Dataset: {dataset}, Model: {self.model}")
        # Implement additional build logic as needed
        return self

    def run(self):
        if self.use_mlflow:
            if self.tracking_uri is None:
                raise ValueError("Tracking uri should be specified")
            mlflow.set_tracking_uri(self.tracking_uri)

            if mlflow.get_experiment_by_name(self.experiment_name) == None:
                mlflow.create_experiment(
                    self.experiment_name, self.artifact_location)
                if self.experiment_tags is not None:
                    mlflow.set_experiment_tags(self.experiment_tags)
            mlflow.set_experiment(self.experiment_name)

        y_test_label = self.items[0][4]
        multi_modal_runner = MultiModalRunner(
            library=self.library, multi_modal=self.multi_modal)
        # multi_modal_runner = MultiModalRunner(
        #     library=self.library, model_func=model_func, batch_size=batch_size,  epochs=epochs)
        # multi_modal = TFMultiModal(
        #     model_func=model_func, batch_size=batch_size,  epochs=epochs)  # 100
        multi_modal_runner.set_data(
            self.items, self.train_idx_arr, self.val_idx_arr, y_test_label)
        combinations = self.combinations if self.combinations is not None else []
        result = multi_modal_runner.predict(combinations)
        return result
