# Import built-in libraries
import re
from pathlib import Path
from itertools import repeat

# Import external libraries
import numpy as np
import pandas as pd
import tifffile as tifff
from bs4 import BeautifulSoup

# Import internal libraries
import codex2mc.illumination_corr as illumination_corr
import codex2mc.ome_writer as ome_writer
from codex2mc.templates import info_dic

def merge_dicts(list_of_dicts):
    """
    This function merges a list of dictionaries into a single dictionary where the values are stored in lists.
    Args:
        list_of_dicts (list): list of dictionaries with common keys
    Returns:
        merged_dict (dict): dictionary with the values stored in lists
    """
    merged_dict = {}
    for d in list_of_dicts:
        for key, value in d.items():
            if key in merged_dict:
                merged_dict[key].append(value)
            else:
                merged_dict[key] = [value]
    return merged_dict

def extract_values(target_pattern,
                   strings,
                   number_cast=True):
    """
    This function extracts the values from a list of strings using a regular expression pattern.
    Args:
        target_pattern (str): regular expression pattern
        strings (list): list of strings to extract the values from
        number_cast (bool): if True, the extracted values are cast to integers
    Returns:
        list: list of extracted values
    """
    return [
        (int(m.group(1)) if number_cast else m.group(1))
        if (m := re.search(target_pattern, s))
        else None
        for s in strings
    ]


def extract_metadata(img_info,meta):
    unit='mm'
    unit_exp={'mm':-3,'nm':-9}

    pixel_size_unit=meta["general"]["resolution_nm"]*10**( unit_exp["nm"]-unit_exp[unit] )## nm to mm

    source="B" if img_info["cycle"]==meta["general"]["referenceCycle"] else "S"#B=background, S=signal


    chann_ind=img_info['channel']
    tile_ind=img_info['tile']


    return {
        "source"                    : source, 
        "position_x"                : meta["roi"]["tiles"][tile_ind]["x_mm"],
        "position_y"                : meta["roi"]["tiles"][tile_ind]["y_mm"],
        "position_x_unit"           : unit ,
        "position_y_unit"           : unit ,
        "physical_size_x"           : pixel_size_unit,
        "physical_size_x_unit"      : unit,
        "physical_size_y"           : pixel_size_unit,
        "physical_size_y_unit"      : unit,
        "size_x"                    : meta["general"]["tileWidth_px"] ,
        "size_y"                    : meta["general"]["tileHeight_px"] ,
        "type"                      : 'uint'+ str(meta["general"]["microscopeBitDepth"]) , 
        "significant_bits"          : meta["general"]["microscopeBitDepth"] ,
        "excitation_wavelenght"     : meta["general"]["wavelengths"][chann_ind-1],
        "excitation_wavelenght_unit": "nm",
        "exposure_time"             : meta["cycle"]["channels"][chann_ind]["exposureTime_ms"] ,
        "marker"                    : meta["cycle"]["channels"][chann_ind]["markerName"] ,
        "filter"                    : meta["cycle"]["channels"][chann_ind]["filterName"] 
        }

def cycle_info(cycle_path, platform_pattern):
    """
    This function reads the images produced by the MACSima device and returns the acquisition information
    specified in the image name.

    Args:
        cycle_path (Path): full path to the cycle folder
        platform_pattern (dict): dictionary with the pattern to search in the image name.
        ref_marker (str): marker of reference used for registration

    Returns:
        df (pd.DataFrame): dataframe with the acquisition information, ROI, rack, exposure time etc.
    """

    full_image_paths = list(cycle_path.glob("*.tif"))
    file_names = [x.name for x in full_image_paths]

    info = info_dic(platform_pattern)

    info["full_path"] = full_image_paths
    info["img_name"]  = file_names
    info["cycle"]     = len(full_image_paths)*[int( re.search(r"cyc(.*?)_",cycle_path.stem).group(1))]
    info["roi"]       = len(full_image_paths)*[int( re.search(r"reg(\d+)",cycle_path.stem).group(1) )]

    for feat, value in platform_pattern.items():
        info[feat] = extract_values(
            target_pattern=value, strings=file_names, number_cast=True
        )

    df = pd.DataFrame(info)
    return df


def append_metadata(cycle_info_df,meta):
    """
    This function appends the metadata extracted from the tiff files to the cycle_info dataframe.
    Args:
        cycle_info_df (pd.DataFrame): dataframe with the acquisition information
    Returns:
        pd.DataFrame: dataframe with the metadata appended to the cycle_info dataframe as new columns.
    """
    img_info_rows =[val for key,val in cycle_info_df.to_dict('index').items()]

    pos = list( map( extract_metadata, img_info_rows,repeat(meta) ) )

    for key, val in merge_dicts(pos).items():
        cycle_info_df.insert(loc=cycle_info_df.shape[1], column=key, value=val)

    return cycle_info_df


def conform_markers(mf_tuple,
                    ref_marker='DAPI'):
    """
    This function reorders the markers in the mf_tuple so that the reference marker is the first element.
    Args:
        mf_tuple (tuple): tuple with the markers and filters
        ref_marker (str): reference marker used for registration
    Returns:
        list: list with the markers and filters reordered so that the reference marker is the first element.
    """

    markers = [tup for tup in mf_tuple if ref_marker not in tup[0]]

    for n,tup in enumerate(mf_tuple):
        if ref_marker in tup[0]:
            markers.insert(0, mf_tuple[n] )

    return markers

def init_stack(group,
               no_of_channels):
    """
    This function initializes the stack array with the dimensions of the tiles.
    Args:
        ref_tile_index (int): index of the reference tile
        groupby_obj (pd.DataFrame.groupby): groupby object with the tiles
        marker_filter_map (list): list with the markers and filters
    Returns:
        np.ndarray: array with the dimensions of the stack array (depth, height, width) and the dtype of the
        reference tile.
    """
    aux_array=[ group['size_x'].unique() , group['size_y'].unique(), group['type'].unique() ]
    check_array=np.array( [ len(element) for element in aux_array ] )
    if np.any(check_array>1):
        print("Warning:tiles of these acquisition have no unique value for the following columns: xy-size or data type")
    width, height, data_type = [ element[0] for element in aux_array  ]
    total_tiles = group['tile'].nunique()
    depth = total_tiles * no_of_channels
    
    stack = np.zeros( (depth,int(height),int(width)), dtype=data_type)

    return stack

def cast_stack_name(cycle_no,
                    acq_group_index,
                    marker_filter_map):
    """
    This function creates the name of the stack file.
    Args:
        cycle_no (int): cycle number
        acq_group_index (tuple): tuple with the acquisition information
        marker_filter_map (list): list with the markers and filters
    Returns:
        str: name of the stack file.
    """
    markers=('__'.join([element[0] for element in marker_filter_map ])).replace('/','-')
    filters=('__'.join([element[1] for element in marker_filter_map ])).replace('/','-')
    
    cycle_no = int(cycle_no)

    c = f'{cycle_no:03d}'
 
    roi = acq_group_index[0]
    s= acq_group_index[1]
    m = markers
    f = filters
    img_format = 'ome.tiff'

    # Nicer way to format strings
    name = f'cycle-{c}-src-{s}-roi-{roi}-markers-{m}-filters-{f}.{img_format}'

    return name


def cast_outdir_name(tup):
    """
    This function creates the name of the output directory.
    Args:
        tup (tuple): tuple with the acquisition information
    Returns:
        str: name of the output directory.
    """
    roi = f'{tup[0]:03d}'

    # Nicer way to format strings
    name = f'roi-{roi}'

    return name


def outputs_dic():
    """
    This function initializes the dictionary used to store the outputs of the create_stack function.
    Returns:
        dict: dictionary with the keys 'index', 'array', 'full_path', 'ome' and empty lists as values
    """

    out={
        'index':[],
        'array':[],
        'full_path':[],
        'ome':[],
        }

    return out


def conform_acquisition_group(group,conformed_markers):
    aux=[]
    for tile_id,frame in group.groupby(['tile']):
        aux.extend([ frame.loc[ (frame['marker']==marker) & (frame['filter']==filt)] for marker, filt in conformed_markers ]) 
    group_conformed=pd.concat(aux)

    return group_conformed



def create_stack(cycle_info_df,
                 output_dir,
                 ref_marker='DAPI',
                 hi_exp=False,
                 ill_corr=False,
                 out_folder='raw',
                 extended_outputs=False,
                 dimensions=["roi","source"]):
    """
    This function creates the stack of images from the cycle_info dataframe.
    Args:
        cycle_info_df (pd.DataFrame): dataframe with the acquisition information
        output_dir (Path): full path to the output directory
        ref_marker (str): reference marker used for registration
        hi_exp (bool): if True, only the tiles with the highest exposure time are selected
        ill_corr (bool): if True, the illumination correction is applied
        out_folder (str): name of the output folder
        extended_outputs (bool): if True, the function returns a dictionary with the stack arrays, full paths and ome-xml metadata
    Returns:
        np.ndarray or list: stack array or list with the full paths of the stack files created in the output directory.
    """

    if extended_outputs:
        out = outputs_dic()
    else:
        out = {'output_paths':[]}
    

    acq_group = cycle_info_df.groupby(dimensions)
    acq_index = list( acq_group.indices.keys() )

    for index in acq_index:
        stack_output_dir = output_dir / cast_outdir_name(index) / out_folder
        stack_output_dir.mkdir(parents=True, exist_ok=True)
        group = acq_group.get_group(index)
        #extract list of unique pairs (marker,filter)
        marker_filter_map=group[['marker','filter']].value_counts().index.values
        #conform the pairs (marker,filter) as to have the reference marker in the first place (1st channel) of the list 
        conformed_markers = conform_markers(marker_filter_map, ref_marker)
        stack = init_stack(group, len( conformed_markers))
        conformed_group=conform_acquisition_group(group,conformed_markers)
        ome = ome_writer.create_ome(conformed_group, conformed_markers)
        counter = 0
        groups_of_tiles = conformed_group.groupby(['tile'])
        for tile_id,frame in groups_of_tiles:
            for img_path in frame['full_path'].values:
                stack[counter,:,:] = tifff.imread(Path(img_path))
                counter += 1
        stack_name = cast_stack_name(frame.cycle.iloc[0], index, conformed_markers)

        if ill_corr:
            tag = 'corr_'
            no_of_channels = len(conformed_markers)
            stack = illumination_corr.apply_corr(stack,no_of_channels)
        else:
            tag = ''

        stack_file_path = stack_output_dir / f'{tag}{stack_name}'

        if extended_outputs:
            out['index'].append(index)
            out['array'].append(stack)
            out['full_path'].append(stack_file_path)
            out['ome'].append(ome)
        else:
            out['output_paths'].append(stack_output_dir)
            tifff.imwrite( stack_file_path , stack, photometric='minisblack' )
            ome,ome_xml = ome_writer.create_ome(group, conformed_markers)
            tifff.tiffcomment(stack_file_path, ome_xml)
        
    if extended_outputs:
        return out
    else:
        return np.unique( out['output_paths'] )
