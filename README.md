# Merge Petriflow XML files

## Description

Combines all the XML files in the current directory into one XML file. Moves Petri Nets next to each other and changes
ids of elements. Order is based on alphabetical order of the XML names.

## Usage

1. Install required packages: ```pip install xmltodict```
2. Create your nets in the top left corner ```https://next.builder.netgrif.com/modeler```
3. Export XML files
5. Move XML file to the ```src``` folder.
6. Run ```python main.py --folder= --count=X``` where count is number of files to merge
7. Import generated XML file to the website

### Parameters

- ```folder``` - merge files in folder
- ```count``` - number of files to merge
- ```xmls``` - paths to xml files if not merging all
- ```how``` - how to merge if mering only two - [vertically, horizontally]
- ```output``` - path to output file
- ```help``` - show help

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

Be careful when merging vertically as the board only supports up to 5000px vertically.