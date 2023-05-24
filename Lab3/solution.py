from __future__ import annotations
from math import *
import os, codecs, copy, sys

class DataRow:
    features : list[str]
    label : str

    def __init__(self, features : list[str], label : str) -> None:
        self.features = features
        self.label = label

class DataSet:
    data_rows : list[DataRow]
    features : list[str]
    features_description : dict[str, set[str]]
    goal_name : str
    goal_description : set[str]
    def __init__(self, header : list[str], data : list[list[str]]) -> None:
        self.features = header[:-1]
        self.goal_name = header[-1]
        self.features_description = {}
        self.goal_description = set()
        self.data_rows = []
        for name in self.features:
            self.features_description[name] = set()
        for data_row in data:
            self.data_rows.append(DataRow(data_row[:-1], data_row[-1]))
            for name, value in zip(self.features, data_row[:-1]):
                self.features_description[name].add(value)
            self.goal_description.add(data_row[-1])
    
    def dataSet(self, x : str, v : str):
        data_set_v = copy.deepcopy(self)
        index = self.features.index(x)
        data_set_v.features.remove(x)
        data_set_v.features_description.pop(x)
        data_rows = []
        for data_row in data_set_v.data_rows:
            if v == data_row.features[index]:
                data_row.features.pop(index)
                data_rows.append(data_row)
        data_set_v.data_rows = data_rows
        return data_set_v
    
    def size(self) -> int:
        return len(self.data_rows)
    
    def size_y(self, y) -> int:
        rows = []
        for data_row in self.data_rows:
            if data_row.label == y:
                rows.append(data_row)
        return len(rows)


class Node:
    type : str
    v : str
    subtrees : list[tuple[str, Node]]
    def __init__(self, type : str, v : str, subtree : list[tuple[str, Node]] = None):
        self.type = type
        self.v = v
        self.subtrees = subtree
    
    def print(self, depth = 1, string = ""):
        if self.type == "leaf":
            print(string + self.v)
        else:
            for subtree in self.subtrees:
                subtree[1].print(depth+1, string + f"{depth}:{self.v}={subtree[0]} ")
    
    def predict(self, data_set : DataSet, features : list[str], inputs: list[str]) -> str:
        if self.type == "leaf":
            return self.v
        else:
            index = features.index(self.v)
            for subtree in self.subtrees:
                if subtree[0] == inputs[index]:
                    new_data_set = data_set.dataSet(self.v, subtree[0])
                    return subtree[1].predict(new_data_set, features, inputs)
            args = {}
            for y in data_set.goal_description:
                args[y] = 0
            for data_row in data_set.data_rows:
                args[data_row.label] += 1
            max_value = max(args.values())
            max_keys = [key for key, value in args.items() if value == max_value]
            return min(max_keys)

class ID3:
    depth : int
    tree : Node
    training_data : DataSet
    def __init__(self, depth : int = None):
        self.depth = depth
        self.tree = None
    
    def P(self, data_set : DataSet, y : str) -> float:
        total = len(data_set.data_rows)
        n = 0
        for data_row in data_set.data_rows:
            if data_row.label == y:
                n += 1
        return float(n / total)

    def E(self, data_set : DataSet) -> float:
        if data_set.size() == 0:
            return 0
        sum = 0
        for y in data_set.goal_description:
            probability = self.P(data_set, y)
            if probability == 0:
                continue
            sum -= (probability * log2(probability))
        return sum
    
    def IG(self, data_set : DataSet, x : str) -> float:
        size = data_set.size()
        entropy = self.E(data_set)
        for v in data_set.features_description[x]:
            data_set_v = data_set.dataSet(x, v)
            size_v = data_set_v.size()
            entropy_v = self.E(data_set_v)
            entropy -= float(size_v / size) * entropy_v
        return entropy
    
    def yArgMax(self, data_set : DataSet) -> str:
        args = {}
        for y in data_set.goal_description:
            args[y] = 0
        for data_row in data_set.data_rows:
            args[data_row.label] += 1
        max_value = max(args.values())
        max_keys = [key for key, value in args.items() if value == max_value]
        return min(max_keys)
    
    def xArgMax(self, data_set : DataSet, X : list[str]) -> str:
        args = {}
        for x in X:
            args[x] = self.IG(data_set, x)
        max_value = max(args.values())
        max_keys = [key for key, value in args.items() if value == max_value]
        return min(max_keys)

    def id3(self, D : DataSet, D_parent : DataSet, X : list[str], y : str, depth : int = 0) -> Node:
        if D.size == 0:
            v = self.yArgMax(D_parent)
            return Node("leaf", v)
        v = self.yArgMax(D)
        if len(X) == 0 or D.size() == D.size_y(v):
            return Node("leaf", v)
        if not self.depth == None:
            if self.depth == depth:
                return Node("leaf", v)
        x = self.xArgMax(D, X)
        subtrees = []
        for v in D.features_description[x]:
            new_D = D.dataSet(x, v)
            t = self.id3(new_D, D, new_D.features, y, depth+1)
            subtrees.append((v,t))
        return Node("node", x, subtrees)
    
    def fit(self, data_set : DataSet):
        self.training_data = data_set
        self.tree = self.id3(data_set, data_set, data_set.features, data_set.goal_name)
        print("[BRANCHES]:")
        self.tree.print()

    def predict(self, data_set : DataSet):
        string = "[PREDICTIONS]:"
        total = len(data_set.data_rows)
        count = 0
        goal_varijables = sorted(list(data_set.goal_description))
        confusion_matrix = {}
        for i in goal_varijables:
            confusion_matrix[i] = {}
            for j in goal_varijables:
                confusion_matrix[i][j] = 0
        for data_row in data_set.data_rows:
            prediction = self.tree.predict(self.training_data, data_set.features, data_row.features)
            true_value = data_row.label
            string += f" {prediction}"
            if prediction == true_value:
                count += 1
            confusion_matrix[true_value][prediction] += 1
        print(string)
        accuracy = round(float(count / total), 5)
        accuracy = '{:.5f}'.format(accuracy)
        print(f"[ACCURACY]: {accuracy}")
        print("[CONFUSION_MATRIX]:")
        for i in goal_varijables:
            string = ""
            for j in goal_varijables:
                string += " " + str(confusion_matrix[i][j])
            print(string)



with codecs.open("Test/" + sys.argv[1], "r", "utf-8") as f:
    header = f.readline().split(",")
    header = ["".join(word.splitlines()) for word in header]
    data = f.readlines()
    data = ["".join(line.splitlines()).split(",") for line in data]
train_dataset = DataSet(header, data)

data = []
with codecs.open("Test/" + sys.argv[2], "r", "utf-8") as f:
    header = f.readline().split(",")
    header = ["".join(word.splitlines()) for word in header]
    data = f.readlines()
    data = ["".join(line.splitlines()).split(",") for line in data]
test_dataset = DataSet(header, data)

if len(sys.argv) == 4:
    model = ID3(int(sys.argv[3]))
else:
    model = ID3()
model.fit(train_dataset)
model.predict(test_dataset)
