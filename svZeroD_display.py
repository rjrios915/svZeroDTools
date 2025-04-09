import matplotlib.pyplot as plt
import time
import pysvzerod

# Output all PV loops seperately
def seperatePVLoops(result):
    valves = {"left_atrium":":mitral", "left_ventricle":":aortic", "right_atrium":":tricuspid", "right_ventricle":":pulmonary"}
    for chamber in valves:
        result.plot(x="Vc:"+chamber, y="pressure:"+chamber+valves[chamber], label=chamber).get_legend().remove()
        plt.title(f"{chamber} PV Curve")
        plt.xlabel(f"{chamber}  Volume (mL)")
        plt.ylabel(f"{chamber} Pressure (mmHg)")
        # plt.savefig(chamber)
    plt.show()

# Plots ventricle and atrial PV loops
# Assumes all four chambers are present uses physiological names
def combinedPVLoops(result):
    a = result.plot(x='Vc:left_atrium',y='pressure:left_atrium:mitral', label="left atrium")
    result.plot(x='Vc:right_atrium',y='pressure:right_atrium:tricuspid',ax=a, label="right atrium")

    plt.title("Atria PV Curves")
    plt.xlabel("Atrial Volume (mL)")
    plt.ylabel("Artial Pressure (mmHg)")

    a = result.plot(x='Vc:left_ventricle',y='pressure:left_ventricle:aortic',  label="left ventricle")
    result.plot(x='Vc:right_ventricle',y='pressure:right_ventricle:pulmonary',ax=a, label="right ventricle")

    plt.title("Ventricle PV Curve")
    plt.xlabel("Ventricle Volume (mL)")
    plt.ylabel("Ventricle Pressure (mmHg)")
    plt.show()

# Convert results into a np dataframe
def formatData(result):
    names = result["name"].unique()
    pressures = [name for name in names if "pressure" in name]
    flows = [name for name in names if 'flow' in name]
    mask = result['name'].isin(names)
    temp = (result[mask]).pivot(index='time', columns='name', values='y').reset_index()

    # Converts to L and mmHg
    temp[pressures] *= 1/1333
    temp[flows] *= 60/1000
    return temp

def print_data(result, time=0):
    dic = result.iloc[time].to_dict()
    for elem in dic:
        print(f"\"{elem}\": {dic[elem]},")

# Plot flow versus time of selected elements
def flowVsTime(result, branch_names):
    branches = ["flow:" + x for x in branch_names]
    fig, bx = plt.subplots()
    for branch in branches:
        result.plot(x="time", y=branch, ax=bx, title="Flow (L/min) vs. Time")
    plt.ylabel("Flow (L/min)")
    plt.xlabel("Time (seconds)")

# Plot pressure versus time of selected elements
def pressureVsTime(result, branch_names):
    branches = ["pressure:" + x for x in branch_names]
    fig, bx = plt.subplots()
    for branch in branches:
        result.plot(x="time", y=branch, ax=bx, title="Pressure (mmHg) vs. Time")
    plt.ylabel("Pressure (mmHg)")
    plt.xlabel("Time (seconds)")

# Plots model based on command line arguments
def main():
    print("Hello! Please make sure to specify file name and targets in svZeroD_display.py!")
    file = "/Users/ricky/Desktop/BMC_Research/banding_models/surrogate_pulHypertensionTruncated_closed.json"
   
    # Targets to visualize 
    targets = ["RPA:J0a", "LPA:J0b", "right_ventricle:pulmonary"]
    result = formatData(pysvzerod.simulate(file))
    
    print("Choose desired fucntion:")
    print("(1) Simulation Runtime\n(2) Combined PV Loops\n(3) Seperate PV Loops\n(4) Flow\n(5) Pressure\n(6) Pressure and Flow\n(7) Quit")
    while(True):
        function = input("Enter number: ")
        if function == "1":
            start_time = time.time()
            pysvzerod.simulate(file)
            end_time = time.time()
            # Calculate the runtime
            print(f"Function runtime: {end_time - start_time} seconds")
        elif function == "2":
            combinedPVLoops(result)
        elif function == "3":
            seperatePVLoops(result)
        elif function == "print_data":
            print_data(result)
        elif function == "4":
            flowVsTime(result, targets)
            plt.show()
        elif function == "5":
            pressureVsTime(result, targets)
            plt.show()
        elif function == "6":
            flowVsTime(result, targets)
            pressureVsTime(result, targets)
            plt.show()
        elif function == "7":
            break
        else:
            print("Please enter a number between 1-6")

if __name__ == "__main__":
    main()