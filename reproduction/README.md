# Reproduction README

## Model summary

This study models Points-of-Dispensing (PODs) in New York City. These are sites set up during a public health emergency to dispense countermeasures. The authors use evolutionary algorithms combined with discrete-event simulation to explore optimal staff numbers with regards to resource use, wait time and throughput.

## Scope of the reproduction

In this assessment, we attempted to reproduce 8 items: 6 figures and 2 tables.

## Reproducing these results

### Repository overview

```{bash}
├── docker
│   └──  ...
├── inputs
│   └──  ...
├── python_outputs
│   └──  ...
├── python_scripts
│   └──  ...
├── r_outputs
│   └──  ...
├── r_scripts
│   └──  ...
├── renv
│   └──  ...
├── tests
│   └──  ...
├── .Rprofile
├── environment.yml
├── README.md
├── renv.lock
└── reproduction.Rproj
```

* `docker/` - Instructions for creation of Docker container.
* `inputs/` - Nine `.txt` files with parameters for pre-screening
* `python_outputs/` - Results for each experiment
* `python_scripts/` - Python code to run experiments with evolutionary algorithms and discrete-event simulation
* `r_outputs/` - Tables and figures
* `r_scripts/` - R code to produce the tables and figures from the model outputs
* `renv/` - Instructions for creation of R environment
* `tests/` - Test to check that model produces consistent results with our reproduction.
* `.Rprofile` - Activates R environment.
* `environment.yml` - Instructions for creation of python environment.
* `README.md` - This file!
* `renv.lock` - Lists R version and all packages in the R environment.
* `reproduction.Rproj` - Project settings.

### Step 1. Set up Python environment

#### Option A: Conda/mamba environment

A `conda`/`mamba` environment has been provided. To create this environment on your machine, you should run this command in your terminal:

```
conda env create -f environment.yml
```

You can then use this environment in your preferred IDE, such as VSCode (where you will be asked to select the kernel/interpreter). You can activate it in the terminal by running:

```
conda activate hernandez2015
```

You can run either of these commands also using `mamba` instead (e.g. `mamba activate hernandez2015`).

#### Option B: Build local docker image

A `Dockerfile` is provided, which you can use to build the Docker image. The docker image will include the correct version of Python and the packages, allow you to run the scripts from the command line.

For this option (and option C), you'll need to ensure that `docker` is installed on your machine.

To create the docker image and then open jupyter lab:

1. In the terminal, navigate to parent directory of the `reproduction/` folder
2. Build the image:

```
sudo docker build --tag hernandez2015 . -f ./reproduction/docker/Dockerfile
```

3. Create a docker container from that image:

```
sudo docker run -it --name hernandez2015_docker hernandez2015
```

#### Option C: Pull pre-built docker image

Pull pre-built docker image

A pre-built image is available on the GitHub container registry. To use it:

1. Create a Personal Access Token (Classic) for your GitHub account with `write:packages` and `delete:packages` access
2. On terminal, run the following command and enter your sudo password (if prompted), followed by the token just generated (which acts as your GitHub password)

```
sudo docker login ghcr.io -u githubusername
```

3. Download the image:

```
sudo docker pull ghcr.io/pythonhealthdatascience/hernandez2015
```

4. Create container:

```
sudo docker run -it --name hernandez2015_docker ghcr.io/pythonhealthdatascience/hernandez2015:latest
```

### Step 2. Running the model

#### Option A: Run the `.py` files

To run all the model scenarios, open and execute each of the `Experiment...` files in `python_scripts/`. These are:

* Experiment 1 - Figure 5 and 6 and Appendix A.2
* Experiment 2 - Figure 7
* Experiment 3 - Figure 8
* Experiment 4 - Figure 9
* Experiment 5 - Figure 10
* Experiment A.1 - Table 3

Ensure you are located in the `python_scripts/` directory when running these. Commands used can vary but examples:

```
python -m Experiment1.py
```

Within the docker container:

```
python2.7 Experiment1.py
```

#### Option B: Pytest

One of the experiments (Experiment 5) has been set up as a test, so you can check whether your output matches the expected output. You can run this from the terminal. Ensure that the `hernandez2015` environment is active and that you are in the `tests/` folder. Then run:

```
pytest -W ignore::DeprecationWarning
```

We use `ignore::DeprecationWarning` to prevent a warning that the "oldnumeric module will be dropped in Numpy 1.9". The test should take approximately 10 to 20 seconds to run.

### Step 3. Set up the R environment

An `renv` environment has been provided. To create this environment locally on your machine, you should open the R project with the `renv` package loaded, and then run:

```
renv::restore()
```

In `renv.lock`, you will see the version of R listed. However, renv will not install this for you, so you will need to switch to this yourself if you wish to also use the same version of R. This reproduction has been run in R 4.4.1, and it is possible (although not definite) that later versions of R may not be compatible, or that you may encounter difficulties installing the specified package versions in later versions of R.

### Step 4. Produce the figures and tables

Run `r_scripts/create_figures.Rmd` to produce the tables and figures.

## Reproduction specs and runtime

This reproduced was conducted mostly on an Intel Core i9-13900K with 81GB RAM running Pop!_OS 22.04 Linux.

To run all the experiments, total run time is **9 hours 16 minutes** (556 minutes). 

* Experiment 1 - 4 hours 28 minutes
* Experiment 2 - 58 minutes
* Experiment 3 - 3 hours 13 minutes
* Experiment 4 - 37 minutes
* Experiment 5 - 8 seconds
* Experiment A.1 - 10 seconds

However, it is important to note that:

* This involve running the models within each experiment in parallel, but each of the experiment files seperately. If these are run at the same time (which I could do without issue), then you will be able to run them all within **4 hours 28 minutes** (the longest experiment)
* This has excluded one of the variants for Experiment 3, which I did not run as it had a very long run time (quoted to be 27 hours in the article) and as, regardless, I had not managed to reproduce the other sub-plots in the figure for that experiment

## Citation

To cite the original study, please refer to the reference above. To cite this reproduction, please refer to the `CITATION.cff` file in the parent folder.

## License

This repository is licensed under the MIT License.