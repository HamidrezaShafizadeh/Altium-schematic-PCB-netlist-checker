# Altium Schematic And PCB Netlists Matcher (Or in short ASAPNM :D)
A simple Python script to check whether PCB netlist and Schematic Netlist are identical.
## Dependencies
+ Python 3, from https://www.python.org/
## Usage
1. Open your project in Altium Designer and then open your PCB file. In the Design section, select Netlist and then Create Netlist From Connected Copper.
![Step1](/Step1.png)
2. Now open your schematic file select Netlist For Document from the Design section and save the Netlist in Calay format.
![Step2](/Step2.png)
3. Run the script Altium-Designer-schematic-and-PCB-netlist-matcher.py and enter the address of the Calay Netlist document file. (Calay netlist is stored in the project folder in a folder called Project Outputs for<your_altium_project_name> and its file extension is .NET)
4. Then give the netlist pcb address to the script. At each stage, the script reports the differences between the 2 netlists, and you can view the next message by pressing the enter key.
