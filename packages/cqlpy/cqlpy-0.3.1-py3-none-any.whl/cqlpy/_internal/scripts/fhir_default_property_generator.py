# %%
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional
import json
from xml.etree.ElementTree import Element, fromstring, parse

# %%


def parse_model_file(model_info_file: Path) -> Element:
    return parse(model_info_file).getroot()


def shred_model_info(model_info: Element) -> dict:
    type_infos = model_info.findall("{urn:hl7-org:elm-modelinfo:r1}typeInfo")
    return {
        type_info.attrib["name"]: type_info.attrib["primaryCodePath"]
        for type_info in type_infos
        if "primaryCodePath" in type_info.attrib
    }


def main(file_path: str):
    model_info_file = Path(file_path)
    model_info = parse_model_file(model_info_file)
    default_properties = shred_model_info(model_info)
    return default_properties


# %%
# Files from https://github.com/cqframework/clinical_quality_language/tree/master/Src/java/quick/src/main/resources/org/hl7/fhir

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument("file_path", type=str)
    args = argument_parser.parse_args()
    print(main(args.file_path))

# %%
