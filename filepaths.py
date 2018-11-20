############################################
# If adding new folder add it here to be able to import it.
############################################

# Add the file-structure to paths
import os
import sys


directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "Code"))
sys.path.append(os.path.join(directory, "Objects"))
