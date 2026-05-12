import xml.etree.ElementTree as ET
import copy

"""- orientation, position, acceleration etc. are called items (because xsens calls them items, in the export window)
- The frames of the types identity, tpose and tpose-isb I call header frames"""

class Mvnx_p:
    def __init__(self, path):
        #get data from mvnx source file
        self.tree = ET.parse(path)
        #root is the seccond line in the mvnx file (because the first line is the identifyer string)
        self.root = self.tree.getroot()
        #arrays we need
        #for header frames
        identity_raw = self.root.findall(".//*[@type='identity']")
        tpose_raw = self.root.findall(".//*[@type='identity']")
        tpose_isb_raw = self.root.findall(".//*[@type='identity']")
        #actual header frames
        #identety (the nullpose):
        self.identity = self.build_header_frame_dict(identity_raw)
        #tpose: t-pose as frame
        self.tpose = self.build_header_frame_dict(tpose_raw)
        #tpose-isb:
        self.tpose_isb = self.build_header_frame_dict(tpose_isb_raw)
        #main Data (list of all frames with list of dictionaries with items)
        self.frames = []
        main_raw = self.root.findall(".//*[@type='normal']")
        for element in main_raw:
            self.frames.append(self.build_one_frame_dict(element))

        #create item lists
        self.orientation = []
        self.centerOfMass = []
        self.acceleration = []
        self.angularAcceleration = []
        self.angularVelocity = []
        self.footContacts = []
        self.jointAngle = []
        self.jointAngleErgo = []
        self.jointAngleErgoXZY = []
        self.jointAngleXZY = []
        self.position = []
        self.sensorFreeAcceleration = []
        self.sensorOrientation = []
        self.sensorMagneticField = []
        self.velocity = []

        #write data into item lists
        self.item_list_data()

    #for all items that don't have data groups
    def group_no(self, child):
        return child.text.split()

    #grouping data of items (orientation for example has groups of 4 (x,y,z,w), while others have groups of 3 values that belong together)
    def group(self, child, chunk_size):
        list_all = child.text.split()
        return ([list_all[i:i + chunk_size] for i in range(0, len(list_all), chunk_size)])

    def get_item_content(self, child, item_name):
        #most items have groups of values that belong together (for example orientation: x,y,z,w or position: x,y,z)
        #switch for different grouping
        #TODO: make sure all items are covered
        #TODO: make sure grouping is correct
        switch = {
            "centerOfMass": self.group(child, 3),
            "acceleration": self.group(child, 3),
            "angularAcceleration": self.group(child, 3),
            "angularVelocity": self.group(child, 3),
            "footContacts": self.group_no(child),
            "jointAngle": self.group(child, 3),
            "jointAngleErgoXZY": self.group(child, 3),
            "jointAngleXZY": self.group(child, 3),
            "jointAngleErgo": self.group(child, 3),
            "orientation": self.group(child, 4),
            "position": self.group(child, 3),
            "sensorFreeAcceleration": self.group(child, 3),
            "sensorOrientation": self.group_no(child),
            "sensorMagneticField": self.group(child, 3),
            "velocity": self.group(child, 3)
        }
        if item_name in switch:
            return switch.get(item_name)
        else:
            return self.group_no(child)

    def append_item_dictionary(self, child, frame_dict):
        #"orientation", "position" etc. (xsens calls them items) are part of a long string -> needs extracting
        #first get the correct Element[Str] and make it a String, so it can be modified:
        child_string = str(child)
        #Now get the correct part of the string (it's (hopefully) alsways in between the last } and the last ')
        item_name = child_string[(child_string.rfind("}"))+1:child_string.rfind("'")].strip()
        #append a dictionary with the item_name as key and the list with it's content as value
        frame_dict[item_name] = self.get_item_content(child, item_name)

    def build_header_frame_dict(self, raw):
        header_frame_dict = {}
        for element in raw:
            for child in element: #goes through every item of the header frame
                self.append_item_dictionary(child, header_frame_dict)
        return header_frame_dict

    #building one frame as a list of dictionaries of items
    def build_one_frame_dict(self, raw):
        one_frame_dict = {}
        for element in raw: #goes through the items of the frame
            self.append_item_dictionary(element, one_frame_dict)
        return one_frame_dict

    #write data from frame into the item lists
    def item_list_data(self):
        if "orientation" in self.frames[0]:
            self.orientation = [copy.deepcopy(d["orientation"]) for d in self.frames]
        if "centerOfMass" in self.frames[0]:
            self.centerOfMass = [copy.deepcopy(d["centerOfMass"]) for d in self.frames]
        if "acceleration" in self.frames[0]:
            self.acceleration = [copy.deepcopy(d["acceleration"]) for d in self.frames]
        if "angularAcceleration" in self.frames[0]:
            self.angularAcceleration = [copy.deepcopy(d["angularAcceleration"]) for d in self.frames]
        if "angularVelocity" in self.frames[0]:
            self.angularVelocity = [copy.deepcopy(d["angularVelocity"]) for d in self.frames]
        if "footContacts" in self.frames[0]:
            self.footContacts = [copy.deepcopy(d["footContacts"]) for d in self.frames]
        if "jointAngle" in self.frames[0]:
            self.jointAngle = [copy.deepcopy(d["jointAngle"]) for d in self.frames]
        if "jointAngleErgo" in self.frames[0]:
            self.jointAngleErgo = [copy.deepcopy(d["jointAngleErgo"]) for d in self.frames]
        if "jointAngleErgoXZY" in self.frames[0]:
            self.jointAngleErgoXZY = [copy.deepcopy(d["jointAngleErgoXZY"]) for d in self.frames]
        if "jointAngleXZY" in self.frames[0]:
            self.jointAngleXZY = [copy.deepcopy(d["jointAngleXZY"]) for d in self.frames]
        if "position" in self.frames[0]:
            self.position = [copy.deepcopy(d["position"]) for d in self.frames]
        if "sensorFreeAcceleration" in self.frames[0]:
            self.sensorFreeAcceleration = [copy.deepcopy(d["sensorFreeAcceleration"]) for d in self.frames]
        if "sensorOrientation" in self.frames[0]:
            self.sensorOrientation = [copy.deepcopy(d["sensorOrientation"]) for d in self.frames]
        if "sensorMagneticField" in self.frames[0]:
            self.sensorMagneticField = [copy.deepcopy(d["sensorMagneticField"]) for d in self.frames]
        if "velocity" in self.frames[0]:
            self.velocity = [copy.deepcopy(d["velocity"]) for d in self.frames]
