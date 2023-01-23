![MHub Runner (3DSlicer Plugin)](https://github.com/AIM-Harvard/SlicerMHubRunner/blob/master/MRunner/Resources/Icons/Name.png?raw=true)

MHub Runner is a 3D Slicer plugin that seamlessly integrates Deep Learning models from the Medical Hub repository (mhub) into 3D Slicer.

## Medical Hub (mhub)
MHub is a repository for Machine Learning models for medical imaging. The goal of mhub is to make these models universally accessible by containerizing the entire model pipeline and standardizing the I/O interface.

Find out more at [mhub.ai](https://mhub.ai) and check out the mhub [GitHub repository](https://github.com/AIM-Harvard/mhub).

## Installation

This plugin is under active development. To test it in 3D slicer follow these steps:

1. Clone the repository to a local folder.
2. Enable developer mode in 3D Slicer (*3D Slicer > Settings > Developer > Enable developer mode*).
3. Start the Extension Wizzard Module (*3D Slicer > Modules > Developer Tools > Extension Wizard*)
4. In the Extension Wizzard click on *Select Extension*.
5. Navigate to the *SlicerMHubRunner* folder (you cloned it in step 1) and press *open*.
6. The plugin is setup and the *MRunner* module is now available in Slicer. To open it, navigate to *3D Slicer > Modules > Examples > MRunner*.


# Usage

First, open a volume in Slicer on which you want to run the plugin. You can use your own data or the slicer sample data. Slicer sample data can be found at *File > Download Sample Data*, to download a chest CT scan click on *CTChest*. Now open the *MRunner* module (navigate to *3D Slicer > Modules > Examples > MRunner*). You will now see the graphical user interface (GUI) of the module.

![Plugin Module Overview](https://raw.githubusercontent.com/AIM-Harvard/SlicerMHubRunner/master/MRunner/Resources/Icons/PluginOverview.png?token=GHSAT0AAAAAABYHSGFF42PNGDWXS3I3YZR4Y6OSKOA)

The *MRunner* module has four sections. The *model selector* is the **first section** at the top of the GUI. Here you select one of the models from *MHub* that you want to run. The **second section** is the *input selection* where you can select an input volume to load into the model. The **third section** is the *output selection*. Since we are only providing segmentation models for now, you select here where the generated segmentations will be stored. You have several options, for example you can create a new segmentation node or select an existing one which will be overwritten. The **fourth section** offers some *advanced options*. Here may can check the *Use GPU* checkbox to download a cuda-enabled image and run the model with GPU acceleration.

# Important Note

**This repository and plugin are under active development, as is the mhub repository.
Use this plugin with caution and always backup your data. We strongly recommend that you only use the slicer sample data and only use this plugin in a non-production environment.**
