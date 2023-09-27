# AlphaFold Interaction Screens on the TSL HPC


## Expectations and Limitations

    - The workflow assumes that you have just one interactor to test against many proteins of interest, and that they're all short enough to run on AlphaFold without splitting.
    - There is only one machine in the TSL cluster that can handle running AlphaFold. Running many proteins will take a long time. Running a genome will probably be _too_ long for you. Speak to us if you need to do that.
    - The workflow tests fewer models than the standard multimer pipeline (10 not 25) in the interests of speed

## Workflow

 1. Submit sequences to AF on HPC for screening.
    1b. Wait ...
 2. Generate the screen IPTM/avPTM values and output CSV
 3. Generate the screen plot 
 4. Select the sequences you wish to examine further
 5. Extract models and visualisations for those sequences


Each step of the workflow can be run independently, so if you have sequences that interact in more complex ways than just one interactor or that need splitting you can jump straight to Step 2 with a set of Alphafold multimer predictions made using the splitter tool here:
## Running the workflow


Having connected to the HPC, load the tools:

```
source af_interaction_screen-0.0.1
```

### Step 1 - Submitting the sequences to AF on the HPC

To submit the sequences for interaction prediction you will use the `submit_screen` command. This requires

    1. a fasta file of the interactor protein (a file with a single sequence)
    2. a fasta file with the proteins of interest (a file with multiple sequences)
    3. the name of a temporary working folder (doesn't have to exist)
    4. the name of a final output folder (doesn't have to exist)

Note that the record names in the fasta sequence files must not have `|` or `_` characters in (as this confuses AF multimer) so please correct if you have to. The pipeline will check and fail quickly if it finds bad names.

The temporary working folder and final output folder will need to be big, so best to put these in `/tsl/scratch`. Your eventual command line would look like this

```
submit_screen interactor_protein.fa proteins_of_interest.fa /tsl/scratch/my_af_interactions_temp /tsl/scratch/my_af_interactions_out
```

This is the actual AF step so takes ages. You can check the progress of the run using `squeue -u<your user name>`

Note that like other AF jobs on the TSL cluster, only one can run at a time and each interaction prediction counts as a separate job. So other users may be able to jump in the queue while yours are still running. This is a feature and just means that no-one can hog the machine.

### Step 2 - Generate the screen IPTM and avIPTM values

Once the AF runs are complete, you need to extract the interaction information into a summary. All the information you need is in the final output folder from the previous step. So we pass that, and the name of an output file to the `summarise_screen` command. This will run on the HPC (it will submit itself) and take some time to run. 

The command line would look like this

```
summarise_screen /tsl/scratch/my_af_interactions_out screen_summary.csv
```

The output file `screen_summary.csv` is a spreadsheet file that contains all the PTM and iPTM values for the highest ranked models. You can make an interactive plot of it in the next step, or if you prefer to filter or analyse it in other ways just take the file from here and work as you wish.

### Step 3 - Create the plot

Now you have the interaction data summarised, you can make the plot. Use the `make_plot` command and give it the name of the input summary csv and an output .html file

```
make_plot screen_summary.csv summary_plot.html
```

### Step 4

This step is simply examining the results from Steps 2 and 3 to make a short-list of proteins you want to look at closer. Prepare those into a CSV file of the same format as that produced in Step 3.

### Step 5 Extract candidate models and visualise quality of modelling

Once you've inspected the plots and csv and you have candidate interactors that you'd like to further examine, usually for quality of modelling, you can extract specified models and generate quality plots using the `extract_models` command. Before you use this command you'll need to prepare a CSV file of model names. Luckily, this should be formatted just like the `screen_summary.csv` file we've been using, with a run folder in the first column and the best model names in the second (the other columns are ignored). Make sure the file only has information on the rows you're interested in and run it as below, giving it the name of the filtered csv and an output folder to save results in:

```
extract_models filtered_run_folders.csv /tsl/scratch/my_models_of_interest
```

The script will then run through the run folders mentioned in that file, run `alphafold_viz` and pull out the PDBs all to the folder you specify. 


## Future

We are working on a splitter tool for longer proteins. Coming soon!