To evaluate the lexington data:

Step 1: Run readLexingtonData.py
-> It will generate a unique file for each node (e.g., bus) with its gps location at each time interval
-> Note: Generate this file for all Spectrum types

Step 2: Run computeLINKEXISTS.py
-> It will generate the 5-D matrix LINK_EXISTS[V, V, S, T, T]

Step 3: Run STB_main_path.py
-> It will generate the LLC and TLEC path for each node pair in the STB graph

Step 4:
