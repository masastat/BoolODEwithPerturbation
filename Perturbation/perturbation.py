import BoolODE as bo
import numpy as np

def perturbation(    
    model_definition, 
    simulation_time,
    num_cells,
    sampling_time,
    perturbed_transcription, 
    perturbed_translation,
    output_dir,
    output_filename
):
    # Normal simulation
    # parameter settings
    gs = bo.GlobalSettings("data", output_dir, True, False, "heaviside")
    js1 = bo.JobSettings(
    [{
        "name": model_definition[:-4],
        "model_definition": model_definition,
        "model_initial_conditions": model_definition + "_ics.txt",
        "simulation_time": simulation_time,
        "num_cells": num_cells,
        "do_parallel": False,
        "sample_cells": False,
        "perturbation": False,
        "perturbed_transcription": {},
        "perturbed_translation": {},
        "perturbation_input": "", 
        "perturbation_sampling_time": [],
        "perturbation_sampling_filename": ""
    }]
    )
    # simulation
    boolodejobs = bo.BoolODE(job_settings=js1, global_settings=gs, postproc_settings="")
    boolodejobs.execute_jobs()
    print("Normal simulation ... Done")
    print("Starting perturbation simulation...")
    print(perturbed_transcription)
    
    # Perturbation simulation
    if len(perturbed_transcription) != 0:
        for trans in perturbed_transcription:
            print(trans)
            # job実行
            js2 = bo.JobSettings(
            [{
                "name": model_definition[:-4] + "-perturbation-transcription-" + list(trans.keys())[0],
                "model_definition": model_definition,
                "model_initial_conditions": model_definition + "_ics.txt",
                "simulation_time": simulation_time,
                "num_cells": num_cells,
                "do_parallel": False,
                "sample_cells": False,
                "perturbation": True,
                "perturbed_transcription": trans,#{ 'g1': 10.0 },
                #"perturbed_translation": , # 片方を想定
                "perturbation_input": model_definition[:-4] + "/simulations/", #ここが同じなら初期状態も同じ

                "perturbation_sampling_time": sampling_time,
                "perturbation_sampling_filename": output_dir + "/" + output_filename #ここが同じなら出力も同じ
                # こいつをどこに置くかが問題
            }]
            )
            boolodejobs = bo.BoolODE(job_settings=js2, global_settings=gs, postproc_settings="")
            boolodejobs.execute_jobs()
        
    else:
        for trans in perturbed_translation:
            print(trans)
            # job実行
            js2 = bo.JobSettings(
            [{
                "name": model_definition[:-4] + "-perturbation-translation-" + list(trans.keys())[0],
                "model_definition": model_definition,
                "model_initial_conditions": model_definition + "_ics.txt",
                "simulation_time": simulation_time,
                "num_cells": num_cells,
                "do_parallel": True,
                "sample_cells": False,
                "perturbation": True,
                "perturbed_transcription": trans,#{ 'g1': 10.0 },
                #"perturbed_translation": , # 片方を想定
                "perturbation_input": model_definition[:-4] + "/simulations/", #ここが同じなら初期状態も同じ

                "perturbation_sampling_time": sampling_time,
                "perturbation_sampling_filename": output_dir + "/" + output_filename #ここが同じなら出力も同じ
                # こいつをどこに置くかが問題
            }]
            )
            boolodejobs = bo.BoolODE(job_settings=js2, global_settings=gs, postproc_settings="")
            boolodejobs.execute_jobs()
            
    E = np.load(output_dir + "/" + output_filename)
        
    return E
    
#     if isinstance(trans, float):
#         hoge
#         {gene: hoge} list loop
#   elif isinstance(trans, dict):



# Run like this

# user setting
# model_definition = "dyn-linear.txt"
# perturbed_transcription = [] #[{ 'g1': 10.0 }, { 'g2': 10.0 }]
# perturbed_translation = [{ 'g3': 5.0 }, { 'g4': 5.0 }]
# simulation_time = 9 # * 100 step
# num_cells = 20 # = sampling_cells
# sampling_time = [100, 300, 500] # 1~simulation_time*100-1?
# output_dir = "Synthetic-H"
# output_filename = "PerturbationSampling.npy"

# default
# do_parallel = True
# sample_cells = False
# output_dir = "Synthetic-H"

# command
# E = perturbation(
#     model_definition, 
#     simulation_time,
#     num_cells,
#     sampling_time,
#     perturbed_transcription, 
#     perturbed_translation,
#     output_dir,
#     output_filename
# )