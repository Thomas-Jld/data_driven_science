import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import time

# plt.ion()

def date_to_nb(date: str) -> int:
    months = [31,29,31,30,31,30,31,31,30,31,30,31]
    res = int(date.split('-')[2])+ sum(months[:int(date.split('-')[1])-1])
    # print(res)
    return res

def nb_to_date(nb: int) -> str:
    months = [31,29,31,30,31,30,31,31,30,31,30,31]
    if nb <= sum(months[:3]):
        mois = "03"
        jour = nb - sum(months[:2])
    elif nb <= sum(months[:4]):
        mois = "04"
        jour = nb - sum(months[:3])
    else:
        mois = "05"
        jour = 1 + nb - sum(months[:4])
    return f"{jour}-{mois}-2020"



class DynamicUpdate():
    def __init__(self,pop: list, tests: list):
        self.pop = pop
        self.tests = tests


    def on_launch(self):
        self.figure = plt.figure()
        self.ax1 = self.figure.add_subplot(111)

        self.ax1.set_autoscaley_on(True)


    def on_running(self, xdata, ydata, date):

        plt.cla()

        self.ax1.bar(xdata,ydata, color='r')
        self.ax1.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: "%.4f" % x))
        self.ax1.set_xticks(['01','27','50','75','976'])
        self.ax1.set_title(f'Pourcentage de personnes testé positive par département   Date: {nb_to_date(date)}')
        self.ax1.set_xlabel("Numéro de Département")
        self.ax1.set_ylabel("Pourcentage de personne positive")
        plt.draw() 
        plt.pause(2)

        plt.savefig(f"saved_files/{date}.png")

        self.ax1.lines = []
        self.ax1.collections = []


    def instant(self, xdata, ydata):

        plt.cla()

        self.ax1.bar(xdata,ydata, color='grey')
        self.ax1.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: "%.4f" % x))
        self.ax1.set_xticks(['01','27','50','75','95','976'])
        self.ax1.set_title(f'Pourcentage de personnes testé positive par département cumulé sur 2 mois')
        self.ax1.set_xlabel("Numéro de Département")
        self.ax1.set_ylabel("Pourcentage de personne positive")
        plt.draw() 
        plt.pause(2)

        plt.savefig(f"saved_files/Cumul.png")


    def __call__(self):
        self.on_launch()
        dates = list(range(date_to_nb(self.tests["data"][0][1]), date_to_nb(self.tests["data"][-1][1])))
        cum_y = {}
        data = []

        for d in dates:
            data = []
            for r in self.tests["data"]:
                if r[2] == "0" and date_to_nb(r[1]) == d:
                    dpt = r[0]
                    part = round(
                        100*float(r[4])/float(self.pop["E:Total"][self.pop["Dpt_id"].index(r[0])]),
                        3)
                    if dpt in cum_y:
                        cum_y[dpt] += part
                    else:
                        cum_y[dpt] = part

                    data.append([dpt, part])
            data = np.array(data).T
            print(data)
            # data = np.array(
            #     [[r[0], 100*float(r[4])/float(self.pop["Total"][self.pop["Dpt_id"].index(r[0])])]
            #      for r in self.tests if r[2] == "0" and  date_to_nb(r[1]) == d]).T
            # self.on_running(data[0], data[1].astype(float), d)
        self.instant(data[0], cum_y.values())
        return data[0], data[1]


def graph_simple(pop: list, tests: list) -> None:
    figure = plt.figure()
    ax1 = figure.add_subplot(111)
    data = []
    d = date_to_nb(tests["data"][-1][1])
    for r in tests["data"]:
        if r[2] == "0" and date_to_nb(r[1]) == d:
            dpt = r[0]
            part = round(100*float(r[4])/float(pop["E:Total"][pop["Dpt_id"].index(r[0])]),6)
            data.append([dpt, part])
    data = np.array(data).T
    ax1.plot(data[0], data[1].astype(float))
    ax1.set_xticks(['01','27','75','95','976'])
    plt.show()


def get_population_data(path: str) -> dict:
    with open(path, 'r') as f:
        data = f.readlines()
        data = np.array([l.strip().split(';') for l in data]).T
        ordered = {}
        for c in list(data):
            ordered[c[0]] = list(c[1:])
        return ordered
        

def get_tests_data(path: str) -> list:
    with open(path, 'r') as f:
        data = f.readlines()
        data = [l.strip().split(';') for l in data]
        return {"head": data[0], "data":data[1:]}

    
def flatten(tests_data: list):
    last = 'E'
    new_data = []
    for row in tests_data:
        if last == 'E':
            new_data.append(row)
            last = row[2]
        else: 
            for i in range(3,9):
                new_data[-1][i] = str(float(row[i])+float(new_data[-1][i]))
            last = row[2]
    return new_data


if __name__ == "__main__":
    pop_data = get_population_data("pop.csv")
    tests_data = get_tests_data("tests.csv")
    # show_smh(pop_data, tests_data["data"])
    tests_data["data"] = flatten(tests_data["data"])
    d = DynamicUpdate(pop_data, tests_data)
    # graph_simple(pop_data, tests_data)
    d()