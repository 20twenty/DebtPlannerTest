import py
args_str = "-n 8"
#args_str = "-k test_payoff_plan_two_debts"
py.test.cmdline.main(args_str.split(" "))
