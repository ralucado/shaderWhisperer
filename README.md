# Shader Whisperer

## Installation
### Python3
* Install Python3 and remember where.
* Install antlr4-python3-runtime package.
### ANTLR4
* Download the JAR from antlr4 website and remember where. Done.
### Eclipse
* Install Eclipse for java developers
* Install and setup ANTLR4 IDE (help in their repo)
* Install and setup PyDev (help in their website)

## Development
* Start Eclipse. New ANTLR4 project.
* Window -> Preferences -> PyDev -> Interpreters -> Python Interpreter: 
  * Click Config first in PATH. It should do the trick, if not, select python3 manually from your filesystem. 
  * Packages: make sure it found antlr4-python3-runtime
  * Libraries: should point to the python3 lib folders in your system, if not add them manually.
* Window -> Preferences -> PyDev -> Interpreters -> Python Interpreter: 
* Project -> Properties -> Project Facets: Enable project facets and select Java 1.8. Apply and Close.
* Project -> Properties -> Java Build Path -> Libraries -> Add External JARs...: antlr4blabla.jar
* Project -> Properties -> ANTLR4 -> Tool -> Enable project specific settings -> Add: antlr4blabla.jar and select it.
* Project -> Properties -> PyDev - PYTHONPATH -> Add source folder: Add any folders where you store python sources that you want your IDE to find (self explanatory, right?)
