# Import built-in libraries

# Import external libraries
import pandas as pd

# Import internal libraries
import codex2mc.tools as tools
import codex2mc.CLI as CLI
import codex2mc.mc_tools as mc_tools
import codex2mc.json_parser as json_parser
import codex2mc.qc as qc
from codex2mc.templates import codex_pattern

# input_test_folder=Path("D:/codex_data_samples/codex_data_v2/8_Cycle2")
# output_test_folder=Path('D:/test_folder')


def main():
    # Get arguments
    args = CLI.get_args()

    # Assign arguments to variables
    input = args.input
    output = args.output
    ref = args.reference_marker
    basicpy_corr = args.illumination_correction
    out_folder_name = args.output_subdir
    json_details=args.json_file_details
    json_general=args.json_file_general

    # Get cycle info
    cycle_info   = tools.cycle_info(input, codex_pattern(version=1))
    cycle_number = int(cycle_info['cycle'].unique()[0])
    region_number= int(cycle_info['roi'].unique()[0])

    # Parse and curate metadata
    metadata = json_parser.depure_json(json_details,json_general,cycle_number,region_number)

    # Append metadata and calculate qc metrics
    cycle_info = tools.append_metadata(cycle_info,metadata)
    cycle_info = qc.append_qc(cycle_info)

    # Select plane with highest contrast
    #cycle_info=pd.read_csv( "C:/Users/VictorP/Desktop/Postdoc projects/Tsomakidou_Tanevski_Schapiro/output/cycle_002_info_meta_extended_QC.csv" )
    cycle_info=cycle_info.loc[cycle_info.groupby(["channel", "tile"])["contrast_median"].idxmax()]
    #cycle_info.to_csv( args.output / 'cycle_{c}_info_meta_extended_QC.csv'.format(c=f'{cycle_number:03d}'), index=False )
    
    output_dirs = tools.create_stack(
        cycle_info,
        output,
        ref_marker=ref,
        hi_exp=args.hi_exposure_only,
        ill_corr=basicpy_corr,
        out_folder=out_folder_name,
    )
    
    # Save markers file in each output directory
    ref_cycle=metadata["general"]["referenceCycle"]
    for path in output_dirs:
        mc_tools.write_markers_file(path,args.remove_reference_marker,ref_cycle)
    
    if args.write_table:
        qc_output_dir=output / "cycle_info"
        qc_output_dir.mkdir(parents=True, exist_ok=True)
        cycle_info.to_csv( qc_output_dir / 'cycle_{c}.csv'.format( c=f'{ cycle_number:03d}' ), index=False )
    
if __name__ == "__main__":
    main()
