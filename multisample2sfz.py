import zipfile
import os
import xml.etree.ElementTree as ET
import json

def xml_to_sfz(xml_file_path, zip_name):

  tree = ET.parse(xml_file_path)
  root = tree.getroot()

  def element_to_sfz(element, zip_name):
    """Converts an XML element to SFZ code."""
    sfz_code = ""
    #if element.tag == "multisample":
    #  sfz_code += f"\n"
    if element.tag == "sample":
      sfz_code += f"\n<region> "
      sfz_code += f"sample={zip_name}/{element.get('file')} "
      sfz_code += f"pitch_keycenter={element.find('./key').get('root')} "
      sfz_code += f"lokey={element.find('./key').get('low')} "
      sfz_code += f"hikey={element.find('./key').get('high')} "
      sfz_code += f"lovel={element.find('./velocity').get('low')} "
      sfz_code += f"hivel={element.find('./velocity').get('high')} "
      if element.find('./key').get('tune') is not None:
        sfz_code += f"tune={element.find('./key').get('tune')} "
    else:
      None
      #sfz_code += f"{element.tag}={element.text}\n"

    for child in element:
      sfz_code += element_to_sfz(child, zip_name)

    #if element.tag == "multisample":
    #  sfz_code += f"</group>\n"
    return sfz_code

  sfz_data = element_to_sfz(root, zip_name)
  return sfz_data


def extract_multisample(zip_file_path):

  # Get the name of the zip file without the extension
  zip_file_name = os.path.splitext(os.path.basename(zip_file_path))[0]

  # Extract all files from the zip file
  with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()

  # Create a new folder for .wav files
  wav_folder_path = os.path.join(os.path.dirname(zip_file_path), zip_file_name)
  os.makedirs(wav_folder_path, exist_ok=True)

  # Move all .wav files to the new folder
  for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".wav"):
      os.rename(os.path.join(os.path.dirname(zip_file_path), filename), os.path.join(wav_folder_path, filename))
  
  return str(zip_file_name)

sep = os.sep
for filename in os.listdir(os.getcwd()):
  if filename.endswith(".multisample"):
    zip_file_path = str(filename)
    data = xml_to_sfz(f"{os.getcwd()}{sep}multisample.xml", extract_multisample(zip_file_path))
    with open(f"{os.getcwd()}{sep}{os.path.splitext(os.path.basename(zip_file_path))[0]}.sfz", "w") as f:
      f.write(data)
    os.remove(f"{os.getcwd()}{sep}multisample.xml")