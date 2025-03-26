from hd2neo4j.types.mapper_types import VectorStrategies
from hd2neo4j.vectors.strategies.bag_of_words import BagOfWords
from hd2neo4j.vectors.strategies.sentence_transformer import (
    TransformerVectorizer,
)


class VectorManager:
    def __init__(self, strategy: VectorStrategies):
        self.strategy = strategy

    def get_vector(self, data):
        if self.strategy == VectorStrategies.DE.value:
            return TransformerVectorizer().vectorize(data)

        elif self.strategy == VectorStrategies.BoW.value:
            return BagOfWords().vectorize(data)

        else:
            print("The strategy is not yet implemented")
