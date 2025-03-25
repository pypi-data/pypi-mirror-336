# Import external libraries
import json
import numpy as np
from pprint import pprint

def main():
    with open("test_data/metadata/experimentV4.json") as f:
        d = json.load(f)

    for region in d["regions"]:
        tile_dict  = {k: dict(list(v.items())[1:]) for k, v in sorted((e["index"], e) for e in region["tiles"])}

        for tile_id, tile_vals in tile_dict.items():
            param_dct = {
                    "position_x": tile_vals["x"],
                    "position_y": tile_vals["y"],
                    "position_x_unit": None,
                    "position_y_unit": None,
                    "physical_size_x": None,
                    "physical_size_x_unit": None,
                    "physical_size_y": None,
                    "physical_size_y_unit": None,
                    "size_x": d["tileWidth_px"],
                    "size_y": d["tileHeight_px"],
                    "type": d["microscopeBitDepth"],  # bit_depth, is this correct?
                    "significant_bits": None,
                    "emission_wavelenght": None,
                    "excitation_wavelenght": None,
                    "emission_wavelenght_unit": None,
                    "excitation_wavelenght_unit": None,
                }
def estimate_tile_pos_mm(meta):
    
    width_px      = meta["general"]["tileWidth_px"]
    height_px     = meta["general"]["tileHeight_px"]
    overlap       = meta["roi"]["tileOverlap"]
    pixel_size_um = meta["general"]["resolution_nm"]/1000
    x_origin_px   = meta["roi"]["x_um"] / pixel_size_um
    y_origin_px   = meta["roi"]["y_um"] / pixel_size_um
    
    step_factor   = (1-overlap)
    dx_px         = step_factor*width_px
    dy_px         = step_factor*height_px

    x_pix =[ val["x"] for key,val in meta["roi"]["tiles"].items() ]
    y_pix =[ val["y"] for key,val in meta["roi"]["tiles"].items() ]
    x_pix =dx_px * ( np.array(x_pix)-min(x_pix) )
    y_pix =dy_px * ( np.array(y_pix)-min(y_pix) )
    x_pix =x_origin_px + x_pix
    y_pix =y_origin_px + y_pix

    x_mm=x_pix *(pixel_size_um/1000)
    y_mm=y_pix *(pixel_size_um/1000)

    tiles_ ={ key:{"x_mm":x_mm[n] ,"y_mm":y_mm[n] } for n,key in enumerate (meta["roi"]["tiles"].keys() ) }
    meta["roi"]["tiles"]=tiles_
    
    return meta




def depure_json(json_details,json_general,cycle_no,region_no):
    meta={"cycle":None,
         "roi":None,
         "general":{"wavelengths"       :None,
                    "magnification"     :None,
                    "aperture"          :None,
                    "objectiveType"     :None,
                    "tileWidth_px"      :None,  
                    "tileHeight_px"     :None,
                    "microscopeBitDepth":None,
                    "resolution_nm"     :None,
                    "referenceChannel"  :None
                   }
        }
    with open(json_details) as f:
        D = json.load(f)
    with open(json_general) as f:
        G = json.load(f)

    indexify_cycles = { element["index"]:element for element in D["cycles"] }
    indexify_regions= {element["index"]:element for element in D["regions"] }
    
    for i in indexify_cycles.keys():
        indexify_channels={ element["index"]:element for element in indexify_cycles[i]["channels"] }
        indexify_cycles[i]["channels"]=indexify_channels

    for i in indexify_regions.keys():
        indexify_tiles={ element["index"]:element for element in indexify_regions[i]["tiles"] }
        indexify_regions[i]["tiles"]=indexify_tiles


        
    meta["cycle"] =indexify_cycles[cycle_no]
    meta["roi"]   =indexify_regions[region_no]

    for key in meta["general"].keys():
        try:
            meta["general"][key] =G[key]
        except:
            meta["general"][key] =D[key]

    meta_=estimate_tile_pos_mm(meta)
    meta_["general"]["referenceCycle"]=G["referenceCycle"]-1 #substraction of 1 is needed since the experiments.json always starts at 2 for unknown reason
            
    return meta_
