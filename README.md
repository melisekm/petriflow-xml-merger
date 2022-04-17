# Merge Petriflow XML files
showcase https://petriflow-xml-merger.herokuapp.com/

## Description

Combines all the XML files in the current directory into one XML file. Moves Petri Nets next to each other and changes
ids of elements. Order is based on alphabetical order of the XML names.

## Usage

1. Install required packages: ```pip install -r requirements.txt```
2. Create your nets in the top left corner ```https://next.builder.netgrif.com/modeler```
3. Export XML files 
4. Run ```python app.py ```
5. Import XML files. Drag and drop them in positions.
6. Press merge.
7. Import generated XML file to the builder website



## Parameters for cmd app

- ```folder``` - merge files in folder, default current folder
- ```count``` - number of files to merge, default all
- ```positions``` - read numerical positions from file - vertical space gets trunctated
- ```xmls``` - paths to xml files if not merging all
- ```how``` - how to merge if merging only two - [vertically, horizontally]
- ```output``` - path to the output file

## Positions

You can merge two nets vertically or horizontally, so with some creativity you can create any kind of position, but these
are predefined.

- 2 - can be set using ```--how``` parameter
- 3 - can be set using ```--how``` parameter
- 4, 5, 6:

```
+-----+-------+-------+
|  4  |   5   |   6   |
+-----+-------+-------+
| 1 2 | 1 2 3 | 1 2 3 |
| 4 3 |   5 4 | 6 5 4 |
+-----+-------+-------+
```

- if using positions file, first pairs in the columns gets merged vertically,
then if only one row remains, it gets merged horizontally

Be careful when merging vertically as the board only supports up to 5000px.
