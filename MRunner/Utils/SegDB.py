from typing import Optional, List
import os, json, yaml, pandas as pd, numpy as np

# global ressource path (./data)
YMLSEG_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'SegDB')

class DB:
    def __init__(self) -> None:

        # load ressources
        self.categories = pd.read_csv(os.path.join(YMLSEG_DATA_DIR, 'categories.csv')).set_index('CodeValue')
        self.types = pd.read_csv(os.path.join(YMLSEG_DATA_DIR, 'types.csv')).set_index('CodeValue')
        self.modifiers = pd.read_csv(os.path.join(YMLSEG_DATA_DIR, 'modifyers.csv')).set_index('CodeValue')
        self.segmentations = pd.read_csv(os.path.join(YMLSEG_DATA_DIR, 'segmentations.csv')).set_index('id') 

db = DB()

class Item:
    def __init__(self, db: DB) -> None:
        self.db = db
        pass

class Segment:
    def __init__(self, id: str) -> None:

        # lookup id
        self.id = id
        self.data = db.segmentations.loc[id]

    def getID(self) -> str:
        return self.id

    def getCategory(self) -> 'Category':
        category_cv = self.data.category # TODO: fix spelling
        return Category(category_cv) 

    def getType(self) -> 'Type':
        type_cv = self.data.type # TODO: fix spelling
        return Type(type_cv)

    def getModifier(self) -> Optional['Modifier']:
        modifier_cv = self.data.modifyer # TODO: fix spelling
        if np.isnan(modifier_cv):
            return None
        return Modifier(modifier_cv)

    def getName(self) -> str:
        return str(self.data['name'])

    def getColor(self) -> Optional['Color']:
        try:
            rgb = self.data["color"].split(",")
            assert len(rgb) == 3
        except:
            return None

        return Color(*map(int, rgb))

    def __str__(self) -> str:
        c = self.getCategory().getCodeMeaning()
        t = self.getType().getCodeMeaning()
        m = self.getModifier()
        return f"S[{self.getName()}:{c}:{t}:{m.getCodeMeaning() if m is not None else 'n/a'}]"

class Modifier:
    def __init__(self, cv: int) -> None:
        
        # lookup code value
        self.data = db.modifiers.loc[cv]

    def getCodeMeaning(self) -> str:
        return str(self.data['CodeMeaning'])

    def __str__(self) -> str:
        return f"M[{self.getCodeMeaning()}]"

class Type:
    def __init__(self, cv: int) -> None:
        
        # lookup code value
        self.data = db.types.loc[cv]

    def getCodeMeaning(self) -> str:
        return str(self.data['CodeMeaning'])

    def __str__(self) -> str:
        return f"T[{self.getCodeMeaning()}]"

class Category:
    def __init__(self, cv: int) -> None:
    
        # lookup code value
        self.data = db.categories.loc[cv]

    def getCodeMeaning(self) -> str:
        return str(self.data['CodeMeaning'])

    def __str__(self) -> str:
        return f"C[{self.getCodeMeaning()}]"

class Color:
    def __init__(self, r:int, g:int, b:int) -> None:
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def getComponents(self) -> List[int]:
        return [self.r, self.g, self.b]

    def getComponentsAsFloat(self) -> List[float]:
        return [self.r / 255, self.g / 255, self.b / 255]

    def getRed(self) -> int:
        return self.r

    def getGreen(self) -> int:
        return self.g

    def getBlue(self) -> int:
        return self.b


class YMLSEG:
    def __init__(self, config_file: str) -> None:
        
        assert os.path.isfile(config_file), f"Config file not found: {config_file}"
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def getSegmentFile(self, segment: Segment) -> str:
        return self.config["segments"][segment.getID()] 

    def getSegments(self) -> List[Segment]:
        segments: List[Segment] = []
        for segment_id in self.config["segments"]:
            segments.append(Segment(segment_id))
 
        return segments