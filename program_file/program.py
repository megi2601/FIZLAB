import csv
import numpy as np
from math import sqrt, floor, log10
import sympy as sp


# współczynniki Studenta-Fishera dla poziomu ufności 98%
student_fisher_95 = {
    2: 12.706,
    3: 4.303,
    4: 3.182,
    5: 2.776,
    6: 2.447,
    7: 2.365,
    8: 2.306,
    9: 2.262,
    10: 2.228,
}


output_file = ""
rounded_output_file = ""
latex_file = ""


class DataAnalyser:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.measurements = list()
        self.single_params = list()
        self.update_file_names()
        self.init_output_files(output_file, rounded_output_file, latex_file)
        self.read_from_file()

    def print_param_list(self):
        print("[" + ", ".join([p.name for p in self.single_params]) + "]")

    def update_file_names(self):
        global output_file
        output_file = self.file_name.split(".")[0] + "_opracowane.csv"
        global rounded_output_file
        rounded_output_file = self.file_name.split(".")[0] + "_zaokraglone.csv"
        global latex_file
        latex_file = self.file_name.split(".")[0] + "_latex.txt"

    def init_output_files(self, csv_f, csv_rounded, latex):
        fieldnames = ["nazwa", "jednostka", "wartosc", "niepewnosc"]
        with open(csv_f, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        with open(csv_rounded, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        with open(latex, "w") as f:
            pass

    # def return_params(self):
    #     return_params = []
    #     for m in self.measurements:
    #         return_params.extend(m.parameters)
    #     return return_params

    def read_from_file(self):
        fieldnames = ["nazwa", "jednostka", "dokladnosc", "powtorzenia"]
        with open(self.file_name, "r") as f:
            reader = csv.DictReader(f, fieldnames=fieldnames, restkey="pomiary")
            next(reader)
            for row in reader:
                r = list(filter(("").__ne__, row["pomiary"]))
                data = [float(i) for i in r]
                name = row["nazwa"]
                unit = row["jednostka"]
                accuracy = float(row["dokladnosc"])
                repeats = int(row["powtorzenia"])
                m = Measurement(name, unit, accuracy, repeats, data)
                self.measurements.append(m)
                self.single_params.append(m.parameters[0])


class Measurement:
    def __init__(self, name, unit, accuracy, repeats, data) -> None:
        self.name = name
        self.unit = unit
        self.accuracy = accuracy
        self.repeats = repeats
        self.data = data
        self.parameters = list()
        self.avg = None
        self.avg1 = None
        self.delta = None
        self.delta1 = None
        self.calc_avg_std()
        self.create_parameter()

    def calc_avg_std(self):
        self.std = np.std(self.data) / sqrt(len(self.data))
        self.avg = np.mean(self.data)
        if len(self.data) <= 10:
            self.std *= student_fisher_95[len(self.data)]
        self.delta = sqrt(self.std ** 2 + (self.accuracy ** 2) / 3)

    def create_parameter(self):
        if self.repeats == 1:
            p = Parametr(self.name, self.avg, self.delta, self.unit)
            self.parameters.append(p)
            p.write_to_file()
        else:
            self.divide_into_one()

    def divide_into_one(self):
        self.avg1 = self.avg / self.repeats
        self.delta1 = self.delta / self.repeats
        new_name = f"{self.name}x{self.repeats}"
        p10 = Parametr(new_name, self.avg, self.delta, self.unit)
        p1 = Parametr(self.name, self.avg1, self.delta1, self.unit)
        self.parameters.extend([p1, p10])
        p1.write_to_file()
        p10.write_to_file()


class Parametr:
    def __init__(
        self,
        name,
        val=0,
        delta=0,
        unit=None,
        expr=None,
    ) -> None:
        self.name = name
        self.symbol = sp.sympify(self.name)
        self.val = val
        self.delta = delta
        self.unit = unit
        self.expr = expr

    def change_unit(self, factor, unit=None):
        self.val *= factor
        self.delta *= factor
        if unit:
            self.unit = unit
        else:
            self.unit += f"*{factor}"
        self.write_to_file()

    def expr(self, expr):
        self.expr = expr

    def write_to_file(self):
        fieldnames = ["nazwa", "jednostka", "wartosc", "niepewnosc"]
        vals = {
            "nazwa": self.name,
            "jednostka": self.unit,
            "wartosc": self.val,
            "niepewnosc": self.delta,
        }
        self.write_row(output_file, fieldnames, vals)
        self.write_row(rounded_output_file, fieldnames, vals, rounded=True)

    def write_row(self, file, fieldnames, vals, rounded=False):
        if rounded:
            n = self.find_rounding_pos(float(vals["niepewnosc"]))
            if n > 0:
                vals["wartosc"] = f'{round(float(vals["wartosc"]), n):.{n}f}'
                vals["niepewnosc"] = f'{round(float(vals["niepewnosc"]), n):.{n}f}'
            else:
                vals["wartosc"] = round(float(vals["wartosc"]), n)
                vals["niepewnosc"] = round(float(vals["niepewnosc"]), n)
        with open(file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(vals)

    def find_rounding_pos(self, num):
        return -int(floor(log10(abs(num)))) + 1

    def calculate(self, dict):
        val, delta = self.expr.evaluate(dict)
        self.val = val
        self.delta = delta
        if not self.unit:
            # self.eval_unit(dict)
            pass
        self.write_to_file()
        return self

    # def eval_unit(self, dict):
    #     units_dict = {key: val.unit for key, val in dict.items()}
    #     # units = set(units_dict.values())
    #     units_expr = self.expr.expr.subs(units_dict)
    #     # l = []
    #     # for e in units:
    #     #     for x in units_expr.args:
    #     #         if e in [str(y) for y in x.free_symbols]:
    #     #             l.append(x)
    #     # unit = sp.Mul(*l)
    #     if sp.srepr(units_expr)[0:3] == "Mul":
    #         l = list(units_expr.args)
    #     else:
    #         l = [x.args for x in list(units_expr.args)]
    #         l = [el for sub in l for el in sub]
    #     for el in l:
    #         try:
    #             float(el)
    #             l.remove(el)
    #         except:
    #             pass
    #     unit = sp.Mul(*l)
    #     self.unit = unit


class Expression:
    def __init__(self, expr, description="", symbols=None) -> None:
        self.expr = expr
        if not symbols:
            self.symbols = expr.free_symbols
        else:
            self.symbols = symbols
        self.description = description
        self.derivatives = dict()
        self.delta = None
        self.differenciate()
        self.delta_expr()
        self.export_to_latex()

    def export_to_latex(self):
        with open(latex_file, "a") as f:
            f.write(f"{self.description}\n\n")
            f.write(f"{sp.latex(self.expr)}\n\n")
            f.write("Pochodne:\n")
            for key, val in self.derivatives.items():
                f.write(f"po {key}:\n{sp.latex(val)}\n")
            f.write("\nRozniczka zupelna:\n")
            f.write(sp.latex(self.delta))
            f.write("\n\n")

    def evaluate(self, dict):
        vals = {el: dict[el].val for el in dict}
        deltas = {sp.Symbol(f"\\Delta {el}"): dict[el].delta for el in dict}
        all = vals | deltas
        val = self.expr.subs(vals).evalf()
        delta = self.delta.subs(all).evalf()
        return val, delta

    def differenciate(self):
        for el in self.symbols:
            diff = self.expr.diff(el)
            self.derivatives[el] = diff

    def delta_expr(self):
        deltas = {el: sp.Symbol(f"\\Delta {el}") for el in self.symbols}
        sum = 0
        for el in self.symbols:
            sum += (self.derivatives[el] * deltas[el]) ** 2
        self.delta = sp.sqrt(sum)
