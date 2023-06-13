"""
-------------------------------------------------
MedicalHub - Repository Wrapper Class (v2)
-------------------------------------------------

-------------------------------------------------
Author: Leonard Nürnberg
Email:  leonard.nuernberg@maastrichtuniversity.nl
-------------------------------------------------
"""

from typing import List, Optional, Union, Any
from enum import Enum

import os, json
from segdb.classes import Segment, Color

class Repository:

    models: Optional[List['RepositoryModel']] = None
    
    def __init__(self, repo_json_file: str) -> None:
        
        # load repo
        assert os.path.isfile(repo_json_file), f"Repository file not found {repo_json_file}"
        with open(repo_json_file, 'r') as f:
            self.data = json.load(f)

    def getModels(self, refresh: bool = False) -> List['RepositoryModel']:
        assert 'models' in self.data, "Invalid repository file"
        if self.models is None or refresh:
            self.models = []
            for model_name, model_data in self.data['models'].items():

                # check if model has a slicer flow
                if not ('flows' in model_data and 'slicer' in model_data['flows']):
                    continue

                # add model
                self.models.append(RepositoryModel(repo=self, data=model_data))
        return self.models

    def getModelNames(self) -> List[str]:
        return list(map(lambda x: f"{x['name']} ({x['tag']})", self.data['models']))

    def getModelById(self, id: str) -> Optional['RepositoryModel']:
        for model_data in self.data['models']:
            if model_data['id'] == id:
                return RepositoryModel(repo=self, data=model_data)
        return None

    def getModelByName(self, name: str) -> Optional['RepositoryModel']:
        for model_data in self.data['models']:
            if model_data['name'] == name:
                return RepositoryModel(repo=self, data=model_data)
        return None


class RepositoryModelType(Enum):
    UNKNOWN = "unknown"
    SEGMENTATION = "segmentation"
    CLASSIFICATION = "classification"


class RepositoryModel:

    def __init__(self, repo: Repository, data: Any) -> None:
        self.repo = repo
        self.data = data

    def getName(self) -> str:
        return str(self.data['name'])

    def getLabel(self) -> str:
        label = str(self.data['label'])
        label = label.replace("<br/>", "").replace("\n", "")
        return label
    
    def getDescription(self) -> str:
        return str(self.data['description'])
    
    def getReferencesText(self, spacer: str = "\n") -> str:
        return spacer.join(self.data['references'])
    
    def getText(self) -> Optional[str]:
        return f"{self.getDescription()}\n\n{self.getReferencesText()}"

    def getType(self) -> RepositoryModelType:
        type = RepositoryModelType.SEGMENTATION if 'segmentation' in self.data else RepositoryModelType.UNKNOWN
        return type

    def hasGpuSupport(self) -> bool:
        return 'gpu' in self.data['hwsupport'] and self.data['hwsupport']['gpu']

    def getImageRef(self, useGPU: bool = False) -> str:
        REPOSITORY = "mhubai"
        IMAGE_TAG_CUDA = "cuda11.4" # cuda12.0
        IMAGE_TAG_NOCUDA = "nocuda"

        image_tag = IMAGE_TAG_CUDA
        image_name = self.getName().lower()

        return f"{REPOSITORY}/{image_name}:{image_tag}"
