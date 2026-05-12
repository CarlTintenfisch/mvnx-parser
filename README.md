# To use this mvnx parser
To install this mvnx parser:
```
pip install mvnx_parser
```
To use this tool:
```
import mvnx_parser
my_data = mvnx_parser.Mvnx_p(<path/to/your/mvnx/file.mvnx>)
```
You can then either access the date through the frames list that has all the data of all normal frames, or through the item lists if you want to have all data of one item (for example orientation, or position). You can also get some data from the header frames.
## Normal frames
The **frames** start at 0 and go up to how ever many frames you have -1. Therefore to get for example the 2. frame:
```
my_data.frames[1]
```
To get a whole **item**, for example orientation from the 2. frame:
```
my_data.frames[1]["orientation"]
```
To get the orientation of the first **joint** of the 2. frame: 
```
my_data.frames[1]["orientation"][0]
```
## Item lists
To access all data of one **item** (for example "orientation"):
```
my_data.orientation
```
To get the data of the first **frame** of the item orientation you would write:
```
my_data.orientation[0]
```
## Header frames
There are three frames in the mvnx file written in front of the normal frames with the types: **"identity"**, **"tpose"** and **"tpose-isb"**.  
You can access them by:
```
my_data.identity
my_data.tpose
my_data.tpose_isb
```
If you want to access for example the first **orientation** of tpose:
```
my_data.tpose["orientation"][0]
```

# The data structure
## frames list
frames is the list with all the frames of the type "normal" which are all the frames of the xsens recording. This list contains each frame as a dictionary.  
Here is the structure it uses (Stuff behind a "#" are comments I wrote in here to explain the structure better):
```
[ #list of all frames
  { #dictionary with all item names of one frame as keys and the item data as values
    <item_name01>: 
      [ #list of data or in most cases groups of related data (coordinates with x, y, z or x, y, z, w)
        [x, y, z], [x, y, z], ... #just as an example
      ],
    <item_name02>:
      [ 
        [x, y, z], [x, y, z], ... #just as an example
      ]
    ...
  },
  {...},
  ...
]
```
## item lists
The item lists contain the values of each item per frame. (It's a list of frames with lists of value(groups)).  
It's structure looks like follows (Stuff behind a "#" are comments I wrote in here to explain the structure better):
```
[ #list of frames
  [#list of grouped item values of the first frame
    [x, y, z], #just as example group/list
    [x, y, z],
    [...],
    ...
  ],
  [#list of grouped item values of the second frame
    [x, y, z], #just as example group/list
    [x, y, z],
    [...],
    ...
  ],
  [...],
  ...
]
```

## header dictionaries
The header dicts look like the following:
```
{ #dictionary with item names as keys and their data as values
  <item_name01>: [ #list of data groups
    [x, y, z, w],
    [...],
    ...
  ],
  <item_name02>: [
    [...],
    ...
  ],
  ...
}
```
