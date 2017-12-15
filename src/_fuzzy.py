
# Contains Fuzzy Logic System Classes

import math
import numpy as np
from collections import defaultdict, Counter

class Classifier:
    """Classifier that takes a feature vector as input, produces scalars as output."""
    def __init__(self, inputs, outputs, rules):
        self.inputs = inputs
        self.outputs = outputs
        self.rulebase = Rulebase(rules)
        self.reasoners = dict()
    def reason(self):
        if (len(self.reasoners) > 0):
            return print("Already reasoned")
        for i, output in enumerate(self.outputs):
            self.reasoners[output.name] = Reasoner(
                self.rulebase,
                self.inputs,
                self.outputs,
                i, 201, "centroid")
    def classify(self, dept, email, feature_vector):
        return {
            "words" : email,
            "ratings" : feature_vector,
            "label" : dept,
            "class" : {
                name : round(reasoner.inference(feature_vector)) for name, reasoner in self.reasoners.items()
            }
        }

class TriangularMF:
    """Triangular fuzzy logic membership function class."""
    def __init__(self, name, start, top, end):
        self.name = name
        self.start = start
        self.top = top
        self.end = end
    def calculate_membership(self, x):
        if x <= self.start:
            y = 0
        if x > self.start and x <= self.top:
            y = (x-self.start)/(self.top-self.start)
        if x > self.top and x <= self.end:
            y = (self.end - x)/(self.end - self.top)
        if x > self.end:
            y = 0
        return y

class TrapezoidalMF:
    """Trapezoidal fuzzy logic membership function class."""
    def __init__(self, name, start, left_top, right_top, end):
        self.name = name
        self.start = start
        self.left_top = left_top
        self.right_top = right_top
        self.end = end
    def calculate_membership(self, x):
        if x <= self.start:
            y = 0
        if x > self.start and x <= self.left_top:
            y = (x - self.start)/(self.left_top - self.start)
        if x > self.left_top and x <= self.right_top:
            y = 1
        if x > self.right_top and x <= self.end:
            y = (self.end - x)/(self.end - self.right_top)
        if x > self.end:
            y = 0
        return y

class Variable:
    """General class for variables in an FLS."""
    def __init__(self, name, range, mfs):
        self.name = name
        self.range = range
        self.mfs = mfs
    def calculate_memberships(self, x):
        return {
            mf.name : mf.calculate_membership(x)
            for mf in self.mfs
        }
    def get_mf_by_name(self, name):
        for mf in self.mfs:
            if mf.name == name:
                return mf

class Input(Variable):
    """Class for input variables, inherits
    variables and functions from superclass Variable."""
    def __init__(self, name, range, mfs):
        super().__init__(name, range, mfs)
        self.type = "input"

class Output(Variable):
    """Class for output variables, inherits
    variables and functions from superclass Variable."""
    def __init__(self, name, range, mfs):
        super().__init__(name, range, mfs)
        self.type = "output"

class Rule:
    """Fuzzy rule class, initialized with an antecedent (list of strings),
    operator (string) and consequent (string)."""
    def __init__(self, n, antecedent, operator, consequent):
        self.number = n
        self.antecedent = antecedent
        self.operator = operator
        self.consequent = consequent
        self.firing_strength = 0
    def calculate_firing_strength(self, datapoint, inputs):
        memberships = []

        for a, x, i in zip(self.antecedent, datapoint, inputs):
            if (a == ''):
                memberships.append(0)
                continue

            m = i.get_mf_by_name(a).calculate_membership(x)
            memberships.append(m)

        # Filtering out zero values
        memberships = [x for x in memberships if x]

        if not memberships:
            self.firing_strength = 0

        elif self.operator == "and":
            self.firing_strength = min(memberships)

        elif self.operator == "or":
            self.firing_strength = max(memberships)

        return self.firing_strength

class Rulebase:
    """The fuzzy rulebase collects all rules for the FLS, can
    calculate the firing strengths of its rules."""
    def __init__(self, rules):
        self.rules = rules
    def calculate_firing_strengths(self, datapoint, inputs, outputindex):
        result = Counter()
        for i, rule in enumerate(self.rules):
            consequent = rule.consequent[outputindex]
            if consequent != "":
                fs = rule.calculate_firing_strength(datapoint, inputs)
                if fs > result[consequent]:
                    result[consequent] = fs
            # print('RULE', i+1, consequent, result[consequent])
            print(datapoint, rule.antecedent, result[consequent])
        return result

class Reasoner:
    def __init__(self, rulebase, inputs, output, outputindex, n_points, defuzzification):
        self.rulebase = rulebase
        self.inputs = inputs
        self.output = output
        self.outputindex = outputindex
        self.discretize = n_points
        self.defuzzification = defuzzification
    def inference(self, datapoint):
        # 1. Calculate the highest firing strength found in the rules per
        # membership function of the output variable
        # looks like: {"low":0.5, "medium":0.25, "high":0}
        firing_strengths = self.rulebase.calculate_firing_strengths(
            datapoint, self.inputs, self.outputindex)

        # 1a. Checks that all consequent names (as stored in firingstrenghts) exist in variable definition
        self.check_consequents(firing_strengths)

        # 2. Aggragate and discretize
        # looks like: [(0.0, 1), (1.2437810945273631, 1), (2.4875621890547261, 1), (3.7313432835820892, 1), ...]
        input_value_pairs = self.aggregate(firing_strengths)

        # 3. Defuzzify
        # looks like a scalar
        crisp_output = self.defuzzify(input_value_pairs)
        return crisp_output
    def aggregate(self, firing_strengths):
        # First find where the aggrageted area starts and ends
        agg_start = self.output[self.outputindex].range[0]
        agg_end = self.output[self.outputindex].range[1]

        # Second discretize this area and aggragate
        # note: if a typo is made in consequent-names, these values will be disregarded without notice !!
        aantal = self.discretize
        breedte = (agg_end - agg_start)/(aantal-1)
        input_value_pairs = []
        for n in range(aantal):
            x = agg_start + n * breedte
            # mslijst bevat de membership waarde van de output variabele (met gegeven outputindex)
            mslijst = self.output[self.outputindex].calculate_memberships(x)
            value = 0
            for ms in mslijst:
                ms_min = min(mslijst[ms], firing_strengths[ms])
                value = max(ms_min, value)
            input_value_pairs.append((x, value))
        return input_value_pairs
    def defuzzify(self, input_value_pairs):
        maxms = 0
        crisp_value = 9999
        # crisp_value = 9999 is eigenlijk foutsituatie
        if self.defuzzification =="som":
            for value_pair in input_value_pairs:
                if value_pair[1]>maxms:
                    maxms = value_pair[1]
                    crisp_value = value_pair[0]
        elif self.defuzzification == "lom":
            for value_pair in input_value_pairs:
                if value_pair[1]>=maxms:
                    maxms = value_pair[1]
                    crisp_value = value_pair[0]
        elif self.defuzzification == 'centroid':
            teller = 0
            noemer = 0
            for value_pair in input_value_pairs:
                teller += value_pair[0]*value_pair[1]
                noemer += value_pair[1]
            if noemer == 0:
                # mag beter
                crisp_value = 0
            else:
                crisp_value = teller/noemer
        return crisp_value
    def check_consequents(self, firing_strengths):
        agg_start = self.output[self.outputindex].range[0]
        mslijst = self.output[self.outputindex].calculate_memberships(agg_start)
        for ms in firing_strengths:
            if ms not in mslijst:
                print('WARNING - consequent:', ms, 'does not match outputdefinition')
        return
