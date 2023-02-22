"""
-------------------------------------------------
MedicalHub - Repository Wrapper Class
-------------------------------------------------

-------------------------------------------------
Author: Leonard Nürnberg
Email:  leonard.nuernberg@maastrichtuniversity.nl
-------------------------------------------------
"""

from typing import List, Optional, Union
from enum import Enum

import os, json
from .SegDB import Segment, Color

"""
 "models": [
        {
            "name": "Thresholder",
            "dockerfile": "Thresholder/",
            "tag": "aimi/thresholder:latest",
            "type": "segmentation",
            "config": {},
            "output": [
                {
                    "file": "output.nrrd",
                    "labels": {
                        "1": "Threshold"
                    }
                }
            ]            
        }
    ]
"""

class Repository:
    
    def __init__(self, repo_json_file: str) -> None:
        
        # load repo
        assert os.path.isfile(repo_json_file), f"Repository file not found {repo_json_file}"
        with open(repo_json_file, 'r') as f:
            self.data = json.load(f)

    def getModels(self) -> List['RepositoryModel']:
        models = []
        for model_data in self.data['models']:
            models.append(RepositoryModel(repo=self, data=model_data))
        return models

    def getModelNames(self) -> List[str]:
        return list(map(lambda x: f"{x['name']} ({x['tag']})", self.data['models']))

    def getModelByTag(self, tag: str) -> Optional['RepositoryModel']:
        for model_data in self.data['models']:
            if model_data['tag'] == tag:
                return RepositoryModel(repo=self, data=model_data)
        return None

    def getModelByName(self, name: str) -> Optional['RepositoryModel']:
        for model_data in self.data['models']:
            if model_data['name'] == name:
                return RepositoryModel(repo=self, data=model_data)
        return None


class RepositoryModelType(Enum):
    SEGMENTATION = "segmentation"
    CLASSIFICATION = "classification"


class CustomSegment(Segment):

    def __init__(self, data: any) -> None:
        self.data = data

    # override
    def getID(self) -> str:
        return self.getName()

    # override
    def getCategory(self) -> None:
        return None

    # override
    def getType(self) -> None:
       return None

    # override
    def getModifier(self) -> None:
       return None

    # override
    def getName(self) -> str:
        return str(self.data['name'])

    # override
    def getColor(self) -> Optional['Color']:
        if "color" in self.data:
            return Color(*self.data["color"])
        else:
            return None

class ExpectedOutputFile:
    def __init__(self, data: any) -> None:
        self.data = data

    def getFileName(self) -> str:
        return str(self.data["file"])

    def getLabels(self) -> List['ExpectedOutputFileLabel']:
        labels = []
        for k in self.data["labels"]:
            label = int(k)
            segment_id = self.data["labels"][k]
            labels.append(ExpectedOutputFileLabel(self, label, segment_id))
        return labels

class ExpectedOutputFileLabel:
    def __init__(self, file: ExpectedOutputFile, label: int, segment: Union[str, object]) -> None:
        self.file = file
        self.label = label
        self.segment = segment

    def getSegment(self) -> Segment:
        if isinstance(self.segment, str):
            segment_id = self.segment
            return Segment(segment_id)
        elif isinstance(self.segment, object):
            segment_data = self.segment
            return CustomSegment(segment_data)
        else:
            raise TypeError(f"Invalid segment type {type(self.segment)}. Expect a segment id (str) or custom (object).")

    def getFile(self) -> ExpectedOutputFile:
        return self.file
    
    def getID(self) -> int:
        return self.label


class RepositoryModelDockerfile:
    def __init__(self, model: 'RepositoryModel', data: any) -> None:
        self.model = model
        self.data = data

        # constants (docker tags for cuda and non-cuda version)
        #  separated due to their significant difference in size
        self.REPOSITORY = "mhubai"
        self.IMAGE_TAG_CUDA = "cuda12.0"
        self.IMAGE_TAG_NOCUDA = "nocuda"

    def isGpuUsable(self) -> bool:
        if "gpu" in self.data and isinstance(self.data["gpu"], bool): 
            return self.data["gpu"]
        else:
            return False # NOTE: default value, might be changed to True

    def getImageName(self) -> str:
        return  self.model.getName().lower()

    def getImageTag(self, useGPU: bool = False) -> str:
        return self.IMAGE_TAG_CUDA if useGPU else self.IMAGE_TAG_NOCUDA

    def getImageRef(self, useGPU: bool = False) -> str:
        return self.REPOSITORY + "/" + self.getImageName() + ":" + self.getImageTag(useGPU)

    def isPullableFromRepository(self) -> bool:
        return bool(self.data["pull"])

    def isDownloadableFromRepository(self) -> bool:
        if "download" in self.data:
            if isinstance(self.data["download"], str):
                return True
            elif isinstance(self.data["download"], bool):
                return self.data["download"]
        return False

    def getDownloadBranch(self) -> Optional[str]:
        if "download" in self.data:
            if isinstance(self.data["download"], str):
                return self.data["download"]
            elif isinstance(self.data["download"], bool):
                return "main"
        else: 
            return None

    def getDownloadPath(self, useGPU: bool = False) -> str:
        branch = self.getDownloadBranch()
        assert branch is not None
        mhub_model_dir = self.getImageName()
        image_tag = self.getImageTag(useGPU)
        return f"https://raw.githubusercontent.com/MHubAI/models/{branch}/models/{mhub_model_dir}/dockerfiles/{image_tag}/Dockerfile"
       

class RepositoryModel:

    def __init__(self, repo: Repository, data: any) -> None:
        self.repo = repo
        self.data = data


    def getName(self) -> str:
        return str(self.data['name'])

    def getLabel(self) -> str:
        return str(self.data['label'])

    def getType(self) -> RepositoryModelType:
        return RepositoryModelType(self.data['type'])

    def getDockerfile(self) -> RepositoryModelDockerfile:
        return RepositoryModelDockerfile(self, self.data['dockerfile'])
    
    def getConfig(self) -> None:
        return None

    def getOutputFiles(self) -> List[ExpectedOutputFile]:
        output_files = []

        # short form : {segment_id1: file_name1, segment_id2: file_name2, ...}
        if isinstance(self.data['output'], dict):
            for segment_id in self.data['output']:
                file_name = self.data['output'][segment_id]

                of_data = {
                    "file": file_name,
                    "labels": {
                        "1": segment_id
                    }
                }

                output_files.append(ExpectedOutputFile(of_data))

        # long form : [{"file": file_name1, "labels": {"1": segment_id1|custom}}, ...]
        elif isinstance(self.data['output'], list):
            for of_data in self.data['output']:
                output_files.append(ExpectedOutputFile(of_data))

        return output_files