#!/usr/bin/python

import sys
import os
import re
import os.path
#Project("{9A19103F-16F7-4668-BE54-9A1E7A4F7556}") = "Exp.DriverInfo.Functions", "Exp.DriverInfo.Functions\Exp.DriverInfo.Functions.csproj", "{A96522E8-EE95-46A9-93D9-CE0DBBE6C103}"
#EndProject

projectReg = re.compile("Project\(\"(?P<guid>\{{0,1}([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}\}{0,1})\"\) = \"(?P<ProjectName>[^\"]+)\", \"(?P<ProjectPath>[^\"]+)\".*\nEndProject")

def getSolutions(searchPath):
    solutionFiles = []

    for file in os.listdir(searchPath):
        if file.endswith(".sln"):
            solutionFiles.append(os.path.join(searchPath, file))
        elif os.path.isdir(searchPath + file) :
            subpath = os.path.join(searchPath, file)
            solutionFiles = solutionFiles + getSolutions(subpath)

    return (solutionFiles)

def findExternalReferences(solution):
    solutionDirectory = os.path.dirname(solution)

    if not os.path.isfile(solution):
        print("{0} does not exists".format(solution))
        exit()

    try:
        externalReferences = []
        with open(solution, "r") as solutionFile:
            solutionFileContent = solutionFile.read()
            projects = projectReg.finditer(solutionFileContent)

            for project in projects:
                projectPath = project.group("ProjectPath")
                projectFullPath = os.path.join(solutionDirectory, projectPath)
                projectName = project.group("ProjectName")

                # print("Project {0} is located to {1}".format(projectName, projectFullPath))

                if projectPath.startswith("../"):
                    externalReferences.append(projectPath)
            
            return (externalReferences)

    except Exception as error:
        print(error)
        print ("Could not read file " + solution + "!\n")
        exit()

##############################################################################
### Main #####################################################################
##############################################################################
print("Running")
if not len(sys.argv) == 2:
    print ("usage:\n\t" + sys.argv[0] + " <path-to-analyse>\n\n")
    exit()

# because windows does not handle POSIX paths for calls to exe-files, we replace / with \
# this way passing a relative path in POSIX-style is still possible
searchPath = sys.argv[1].replace("/", os.sep)

if not searchPath.endswith(os.sep):
    searchPath = searchPath + os.sep

# In order to handle windows-executables also check for exe files
if (not os.path.isdir(searchPath)):
    print ("{0} directory not found.".format(searchPath))
    exit()

print("Search for solutions in {0}".format(searchPath))

solutions = getSolutions(searchPath)

for solution in solutions:
    print("Solution found : {0}".format(solution))
    externalDependencies = findExternalReferences(solution)

    if len(externalDependencies) == 0:
        print("No external dependencies")
    else:
        print("Triggers for solution {0}".format(os.path.basename(solution)))
        for externalDependency in externalDependencies:
            print(externalDependency)
        
