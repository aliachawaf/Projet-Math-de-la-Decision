import src.algoExhaustif as algo11
import src.algoReel as algo50
import sys

def main():

    launch_mode = "exhaustif"
    number_results_max = None

    for arg in sys.argv[1:]:
        sub_arg = arg[2:]
        if sub_arg[:3] == "arg":
            launch_mode = sub_arg[4:]
        elif sub_arg[:3] == "num":
            number_results_max = sub_arg[7:]
        elif sub_arg[:3] == "ext":
            ext = sub_arg[4:]

    if launch_mode == "exhaustif":
        algo11.main(number_results_max)
    else:
        algo50.main()

main()
