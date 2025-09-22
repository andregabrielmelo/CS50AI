import csv
from email import header
from encodings import undefined
from itertools import count
from plistlib import InvalidFileException
import sys
from enum import Enum
from turtle import st
from typing import Any, Mapping, TypedDict, cast

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


# Enums
class Month(Enum):
    Jan = 0
    Feb = 1
    Mar = 2
    Apr = 3
    May = 4
    June = 5
    Jul = 6
    Aug = 7
    Sep = 8
    Oct = 9
    Nov = 10
    Dec = 11


class VisitorType(Enum):
    Other = 0
    New_Visitor = 0
    Returning_Visitor = 1


# Type
class Evidence(TypedDict):
    Administrative: int
    Administrative_Duration: float
    Informational: int
    Informational_Duration: float
    ProductRelated: int
    ProductRelated_Duration: float
    BounceRates: float
    ExitRates: float
    PageValues: float
    SpecialDay: float
    Month: int  # Month
    OperatingSystems: int
    Browser: int
    Region: int
    TrafficType: int
    VisitorType: int  # VisitorType
    Weekend: bool


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidences: list[list] = []
    labels: list[int] = []

    # Get evidences and labels
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        for row in csv_reader:
            # Get evidence (first 17 columns)
            evidence: Evidence = {}

            # Map enums
            month = Month[row["Month"]]
            row["Month"] = int(month.value)

            visitor = VisitorType[row["VisitorType"]]
            row["VisitorType"] = int(visitor.value)

            # Map row to evidence
            for key, key_type in Evidence.__annotations__.items():
                evidence[key] = key_type(row[key])
            evidences.append(list(evidence.values()))

            # Get label (last column, 18th)
            if row["Revenue"] == "TRUE":
                labels.append(1)
            elif row["Revenue"] == "FALSE":
                labels.append(0)

    return evidences, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    clf = KNeighborsClassifier(n_neighbors=1)
    clf.fit(evidence, labels)
    return clf


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    true_positive = 0.0
    true_negative = 0.0
    false_positive = 0.0
    false_negative = 0.0
    for actual_value, predicted_value in zip(labels, predictions):
        # true positive
        if actual_value == 1 and actual_value == predicted_value:
            true_positive += 1
        # true negative
        if actual_value == 0 and actual_value == predicted_value:
            true_negative += 1
        # false positive
        if actual_value == 1 and actual_value != predicted_value:
            false_positive += 1
        # false negative
        if actual_value == 0 and actual_value != predicted_value:
            false_negative += 1

    sensitivity = true_positive / (true_positive + false_positive)
    specificity = true_negative / (true_negative + false_negative)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
