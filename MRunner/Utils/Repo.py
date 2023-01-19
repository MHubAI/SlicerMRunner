"""
-------------------------------------------------
MedicalHub - Repository Wrapper Class
-------------------------------------------------

-------------------------------------------------
Author: Leonard Nürnberg
Email:  leonard.nuernberg@maastrichtuniversity.nl
-------------------------------------------------
"""

from typing import List, Optional
from enum import Enum

import os, json
from .SegDB import Segment

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
    pass

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
    def __init__(self, file: ExpectedOutputFile, label: int, segment_id: str) -> None:
        self.file = file
        self.label = label
        self.segment_id = segment_id

    def getSegment(self) -> Segment:
        return Segment(self.segment_id)

    def getFile(self) -> ExpectedOutputFile:
        return self.file
    
    def getID(self) -> int:
        return self.label

class RepositoryModel:

    def __init__(self, repo: Repository, data: any) -> None:
        self.repo = repo
        self.data = data


    def getName(self) -> str:
        return str(self.data['name'])

    def getType(self) -> RepositoryModelType:
        return RepositoryModelType(self.data['type'])

    def getDockerfile(self) -> str:
        return self.data['dockerfile']

    def getDockerTag(self) -> str:
        return self.data['tag']
    
    def getConfig(self) -> None:
        return None

    def getOutputFiles(self) -> List[ExpectedOutputFile]:
        output_files = []
        for of_data in self.data['output']:
            output_files.append(ExpectedOutputFile(of_data))
        return output_files

    #def getSegments(self) -> List[Segment]:
    #    segments = []
    #    for segment_id in self.data['segments']:
    #        segment = Segment(segment_id)
    #        segments.append(segment)
    #    return segments

