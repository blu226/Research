from main import *
from metrics2 import *

def run_epidemic(dir):
    epidemic_simulation(dir)
    epidemic_metrics()


run_epidemic("2007-10-23_2007-10-24/")