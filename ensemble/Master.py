from sklearn.ensemble import GradientBoostingClassifier

from ensemble.Classifier import Classifier
from ensemble.FNCBaseLine import binary_co_occurence, binary_co_occurence_stops, count_grams, polarity_features, \
    refuting_features, word_overlap_features
from utils.score import report_score


class Master(Classifier):
    def __init__(self,dataset):
        super().__init__(dataset)
        self.gbc = GradientBoostingClassifier()

    def predict(self,data):
        lists = list(zip(*data))
        stances = lists[0]
        other_classifiers = list(zip(*lists[1:]))

        Xs, ys = self.xys(stances)

        for i, x in enumerate(Xs):
            Xs[i] = x + list(other_classifiers[i])

        pred = self.gbc.predict(Xs)

        print(report_score(ys,pred))

        return pred

    def fit(self,data):
        lists = list(zip(*data))
        stances = lists[0]
        other_classifiers = list(zip(*lists[1:]))

        Xs,ys = self.xys(stances)


        for i,x in enumerate(Xs):
            Xs[i] = x + list(other_classifiers[i])

        self.gbc.fit(Xs,ys)

    def preload_features(self, stances, ffns=list([
                                               binary_co_occurence,
                                               binary_co_occurence_stops,
                                               count_grams,
                                               polarity_features,
                                               refuting_features,
                                               word_overlap_features])):
        self.fdict = self.load_feats("features/fnc.pickle",stances,ffns)


