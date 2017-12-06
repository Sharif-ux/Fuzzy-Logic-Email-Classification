
# Contains Fuzzy Logic System Classes

import math
import numpy as np
from collections import defaultdict, Counter

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

# Test your implementation by running the following statements
# Enter your answers in the Google form to check them, round to two decimals

triangular_mf = TriangularMF("medium", 150, 250, 350)
print(triangular_mf.calculate_membership(100))
print(triangular_mf.calculate_membership(249))
print(triangular_mf.calculate_membership(300))

trapezoidal_mf = TrapezoidalMF("bad", 0, 0, 2, 4)
print(trapezoidal_mf.calculate_membership(1.2))
print(trapezoidal_mf.calculate_membership(2.3))
print(trapezoidal_mf.calculate_membership(3.9))


class Variable:
    """General class for variables in an FLS."""
    def __init__(self, name, range, mfs):
        self.name = name
        self.range = range
        self.mfs = mfs

    def calculate_memberships(self, x):
        """Test function to check whether
        you put together the right mfs in your variables."""
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


# Input variable for your income
# Your code here
mfs_income = [TrapezoidalMF("low", -100, 0, 200, 400), TriangularMF("medium", 200, 500, 800), TrapezoidalMF("high", 600, 800, 1000, 1200)]
income = Input("income", (0, 1000), mfs_income)

# Input variable for the quality
# Your code here
mfs_quality = [TrapezoidalMF("bad", -1, 0, 2, 4), TriangularMF("okay", 2, 5, 8), TrapezoidalMF("amazing", 6, 8, 10, 12)]
quality = Input("quality", (0, 10), mfs_quality)

# Output variable for the amount of money
# Your code here
mfs_money = [TrapezoidalMF("low", -100, 0, 100, 250), TriangularMF("medium", 150, 250, 350), TrapezoidalMF("high", 250, 400, 500, 600)]
money = Output("money", (0, 500), mfs_money)

inputs = [income, quality]
output = money


# Test your implementation by running the following statements
# Enter your answers in the Google form to check them, round to two decimals

print(income.calculate_memberships(489))
print(quality.calculate_memberships(6))
print(output.calculate_memberships(222))

print(income.name, income.range)
print('inputs:', inputs[0].name, inputs[0].calculate_memberships(489))


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
        # choosen min operator for T-norm
        i = 0
        self.firing_strength = 9999999999999999999
        for input_ms in self.antecedent:
            # print (i, input_ms, datapoint[i])
            mslijst = inputs[i].calculate_memberships(datapoint[i])
            msvalue = mslijst[input_ms]
            self.firing_strength = min(self.firing_strength, msvalue)
            # print (msvalue, self.firing_strength)
            i += 1
        # zou bovenstaand ook kunnen door calculate_memberships of vector van waarden te doen ???
        return self.firing_strength


# Test your implementation by checking the following statements
# Enter your answers in the Google form to check them, round to two decimals

rule1 = Rule(1, ["low", "amazing"], "and", "low")
print(rule1.calculate_firing_strength([200, 6.5], inputs))
print(rule1.calculate_firing_strength([0, 10], inputs))

rule2 = Rule(2, ["high", "bad"], "and", "high")
print(rule2.calculate_firing_strength([100, 8], inputs))
print(rule2.calculate_firing_strength([700, 3], inputs))


from collections import Counter

class Rulebase:
    """The fuzzy rulebase collects all rules for the FLS, can
    calculate the firing strengths of its rules."""
    def __init__(self, rules):
        self.rules = rules

    def calculate_firing_strengths(self, datapoint, inputs):
        result = Counter()
        for i, rule in enumerate(self.rules):
            fs = rule.calculate_firing_strength(datapoint, inputs)
            consequent = rule.consequent
            if fs > result[consequent]:
                result[consequent] = fs
        return result



# Add the rules listed in the question description
# Your code here
rule1 = Rule(1, ["low", "amazing"], "and", "low")
rule2 = Rule(2, ["medium", "amazing"], "and", "low")
rule3 = Rule(3, ["high", "amazing"], "and", "low")
rule4 = Rule(4, ["low", "okay"], "and", "low")
rule5 = Rule(5, ["medium", "okay"], "and", "medium")
rule6 = Rule(6, ["high", "okay"], "and", "medium")
rule7 = Rule(7, ["low", "bad"], "and", "low")
rule8 = Rule(8, ["medium", "bad"], "and", "medium")
rule9 = Rule(9, ["high", "bad"], "and", "high")

# print('testfs: ', rule1.calculate_firing_strength([234, 7.5], inputs))

rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]

rulebase = Rulebase(rules)


# Test your implementation of calculate_firing_strengths()
# Enter your answers in the Google form to check them, round to two decimals

datapoint = [500, 3]
print(rulebase.calculate_firing_strengths(datapoint, inputs))

datapoint = [234, 7.5]
print(rulebase.calculate_firing_strengths(datapoint, inputs))


class Reasoner:
    def __init__(self, rulebase, inputs, output, n_points, defuzzification):
        self.rulebase = rulebase
        self.inputs = inputs
        self.output = output
        self.discretize = n_points
        self.defuzzification = defuzzification

    def inference(self, datapoint):
        # 1. Calculate the highest firing strength found in the rules per
        # membership function of the output variable
        # looks like: {"low":0.5, "medium":0.25, "high":0}
        firing_strengths = rulebase.calculate_firing_strengths(datapoint, inputs)

        # 2. Aggragate and discretize
        # looks like: [(0.0, 1), (1.2437810945273631, 1), (2.4875621890547261, 1), (3.7313432835820892, 1), ...]
        input_value_pairs = self.aggregate(firing_strengths)

        # 3. Defuzzify
        # looks like a scalar
        crisp_output = self.defuzzify(input_value_pairs)
        return crisp_output

    def aggregate(self, firing_strengths):
        # First find where the aggrageted area starts and ends
        # Your code here
        agg_start = self.output.range[0]
        agg_end = self.output.range[1]

        # Second discretize this area and aggragate
        aantal = self.discretize
        breedte = (agg_end - agg_start)/(aantal-1)
        # print(aantal, 'breedte: ', breedte)
        input_value_pairs = []
        for n in range(aantal):
            x = agg_start + n * breedte
            mslijst = self.output.calculate_memberships(x)
            # print('x:', x), print('mslijst: ', mslijst)
            # print('fs: ', firing_strengths)
            value = 0
            for ms in mslijst:
                ms_min = min(mslijst[ms], firing_strengths[ms])
                value = max(ms_min, value)
                # print(ms_min, value)
            # print(value)
            input_value_pairs.append((x, value))
        return input_value_pairs

    def defuzzify(self, input_value_pairs):
        maxms = 0
        crisp_value = 9999
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
        # crisp_value = 9999 is eigenlijk foutsituatie
        return crisp_value


# Test your implementation of the fuzzy inference
# Enter your answers in the Google form to check them, round to two decimals

thinker = Reasoner(rulebase, inputs, output, 201, "som")
datapoint = [100, 1]
# firing_strengths = rulebase.calculate_firing_strengths(datapoint, inputs)
# print("fs(100,1):", firing_strengths)
# print(thinker.aggregate(firing_strengths))
print(round(thinker.inference(datapoint)))

thinker = Reasoner(rulebase, inputs, output, 101, "lom")
datapoint = [550, 4.5]
# firing_strengths = rulebase.calculate_firing_strengths(datapoint, inputs)
# print("fs(550,4.5):", firing_strengths)
print(round(thinker.inference(datapoint)))

thinker = Reasoner(rulebase, inputs, output, 201, "som")
datapoint = [900, 6.5]
# firing_strengths = rulebase.calculate_firing_strengths(datapoint, inputs)
# print("fs(900,6.5):", firing_strengths)
print(round(thinker.inference(datapoint)))

thinker = Reasoner(rulebase, inputs, output, 201, "lom")
datapoint = [100, 1]
print(round(thinker.inference(datapoint)))

thinker = Reasoner(rulebase, inputs, output, 101, "som")
datapoint = [550, 4.5]
print(round(thinker.inference(datapoint)))

thinker = Reasoner(rulebase, inputs, output, 201, "lom")
datapoint = [900, 6.5]
print(round(thinker.inference(datapoint)))
