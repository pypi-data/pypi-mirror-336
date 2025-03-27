'''
    ########################################
    ## Sports2D tests                     ##
    ########################################

    Check whether Sports2D still works after each code modification.
    Disable the real-time results and plots to avoid any GUI issues.

    Usage: 
    cd Sports2D/Utilities
    python tests.py
'''


## INIT
from importlib.metadata import version
import toml
import subprocess
from pathlib import Path


## AUTHORSHIP INFORMATION
__author__ = "David Pagnon"
__copyright__ = "Copyright 2023, Sports2D"
__credits__ = ["David Pagnon"]
__license__ = "BSD 3-Clause License"
__version__ = version("sports2d")
__maintainer__ = "David Pagnon"
__email__ = "contact@david-pagnon.com"
__status__ = "Development"


## FUNCTIONS
def test_workflow():
    '''
    Test the workflow of Sports2D.
    '''

    #############################
    ## From Python             ##
    #############################

    # Default
    config_path = Path.cwd().parent / 'Demo' / 'Config_demo.toml'
    config_dict = toml.load(config_path)
    config_dict.get("project").update({"video_dir":'../Demo'})
    config_dict.get("process").update({"show_realtime_results":False})
    config_dict.get("post-processing").update({"show_graphs":False})
    
    from Sports2D import Sports2D
    Sports2D.process(config_dict)


    #############################
    ## From command line (CLI) ##
    #############################

    # Default
    demo_cmd = ["sports2d", "--show_realtime_results", "False", "--show_graphs", "False"]
    subprocess.run(demo_cmd, check=True, capture_output=True, text=True, encoding='utf-8')

    # With no pixels to meters conversion, no multiperson, lightweight mode, detection frequency, slowmo factor, gaussian filter, RTMO body pose model
    demo_cmd2 = ["sports2d", "--show_realtime_results", "False", "--show_graphs", "False", 
                 "--to_meters", "False", 
                 "--multiperson", "False", 
                 "--mode", "lightweight", "--det_frequency", "50", 
                 "--slowmo_factor", "4",
                 "--filter_type", "gaussian",
                 "--pose_model", "body", "--mode", """{'pose_class':'RTMO', 'pose_model':'https://download.openmmlab.com/mmpose/v1/projects/rtmo/onnx_sdk/rtmo-m_16xb16-600e_body7-640x640-39e78cc4_20231211.zip', 'pose_input_size':[640, 640]}"""]
    subprocess.run(demo_cmd2, check=True, capture_output=True, text=True, encoding='utf-8')
    
    # With a time range, inverse kinematics, marker augmentation, body pose_model and custom RTMO mode
    demo_cmd3 = ["sports2d", "--show_realtime_results", "False", "--show_graphs", "False",
                 "--time_range", "1.2", "2.7",
                 "--do_ik", "True", "--use_augmentation", "True", 
                 "--px_to_m_from_person_id", "1", "--px_to_m_person_height", "1.65",
                 "--visible_side", "front", "auto", "--participant_mass", "55.0", "67.0"]
    subprocess.run(demo_cmd3, check=True, capture_output=True, text=True, encoding='utf-8')
    
    # From config file
    cli_config_path = Path(__file__).resolve().parent.parent / 'Demo' / 'Config_demo.toml'
    config_dict = toml.load(cli_config_path)
    cli_video_dir = Path(__file__).resolve().parent.parent / 'Demo'
    config_dict.get("project").update({"video_dir": str(cli_video_dir)})
    with open(cli_config_path, 'w') as f: toml.dump(config_dict, f)
    demo_cmd4 = ["sports2d", "--config", str(cli_config_path), "--show_realtime_results", "False", "--show_graphs", "False"]
    subprocess.run(demo_cmd4, check=True, capture_output=True, text=True, encoding='utf-8')
