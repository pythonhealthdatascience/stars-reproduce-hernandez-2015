# Hernandez et al. 2015 computational reproducibility assessment <a href="https://github.com/pythonhealthdatascience"><img src="quarto_site/stars_logo_blue.png" align="right" height="120" alt="STARS" /></a>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13832260.svg)](https://zenodo.org/doi/10.5281/zenodo.13832260)

This repository forms part of work package 1 on the project STARS: Sharing Tools and Artefacts for Reproducible Simulations. It assesses the computational reproducibility of:

> Hernandez, I., Ramirez-Marquez, J., Starr, D., McKay, R., Guthartz, S., Motherwell, M., Barcellona, J. **Optimal staffing strategies for points of dispensing**. *Computers & Industrial Engineering* 83 (2015). <https://doi.org/10.1016/j.cie.2015.02.015>.

## Website

⭐ **[Click here to check out the website for this repository](https://pythonhealthdatascience.github.io/stars-reproduce-hernandez-2015/)** ⭐

This website is created using Quarto and hosted using GitHub Pages. It shares everything from this computational reproducibility assessment.

## Protocol

The protocol for this work is summarised in the diagram below and archived on Zenodo:

> Heather, A., Monks, T., Harper, A., Mustafee, N., & Mayne, A. (2024). Protocol for assessing the computational reproducibility of discrete-event simulation models on STARS. Zenodo. <https://doi.org/10.5281/zenodo.12179846>.

![Workflow](./quarto_site/stars_wp1_workflow.png)

## Repository overview

<!-- TODO: Update this if you amend the structure or contents of the repository -->
```bash
├── .github
│   └──  workflows
│        └──  ...
├── evaluation
│   └──  ...
├── logbook
│   └──  ...
├── original_study
│   └──  ...
├── quarto_site
│   └──  ...
├── reproduction
│   └──  ...
├── .gitignore
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── _quarto.yml
├── citation_apalike.apa
├── citation_bibtex.bib
├── index.qmd
└── requirements.txt
```

**Key sections:** These folders have all the content related to the original study and reproduction...

* **`original_study/`** - Original study materials (i.e. journal article, supplementary material, code and any other research artefacts).
* **`reproduction/`** - Reproduction of the simulation model. Once complete, this functions as a research compendium for the model, containing all the code, parameters, outputs and documentation.
* **`evaluation/`** - Quarto documents from the evaluation of computational reproducibility. This includes the scope, assessment of reproduction success, and comparison of the original study materials against various guidelines, and summary report.
* **`logbook/`** - Daily record of work on this repository.

**Other sections:** The remaining files and folders support creation of the Quarto site to share the reproduction, or are other files important to the repository (e.g. `README`, `LICENSE`, `.gitignore`)...

* `.github/workflows/` - GitHub actions.
* `quarto_site/` - A Quarto website is used to share information from this repository (including the original study, reproduced model, and reproducibility evaluation). This folder contains any additional files required for creation of the site that do not otherwise belong in the other folders.
* `.gitignore` - Untracked files.
* `CHANGELOG.md` - Description of changes between GitHub releases and the associated versions on Zenodo.
* `CITATION.cff` - Instructions for citing this repository, created using [CFF INIT](https://citation-file-format.github.io/).
* `CONTRIBUTING.md` - Contribution instructions for repository.
* `LICENSE` - Details of the license for this work.
* `README.md` - Description for this repository. You'll find a seperate README for the model within the `reproduction/` folder, and potentially also the `original_study/` folder if a README was created by the original study authors.
* `_quarto.yml` - Set-up instructions for the Quarto website.
* `citation_apalike.bib` - APA citation generated from CITATION.cff.
* `citation_bibtex.bib` - Bibtex citation generated from CITATION.cff.
* `index.qmd` - Home page for the Quarto website.
* `requirements.txt` - Environment for creation of Quarto site (used by `.github/workflows/quarto_publish.yaml`).

## Citation

Please cite the archived version of this repository on Zenodo:

> Heather, A., Monks, T., & Harper, A. (2025). Hernandez et al. 2015 computational reproducibility assessment. Zenodo. <https://zenodo.org/doi/10.5281/zenodo.13832260>

You can also cite the repository on GitHub. Please refer to the citation file `CITATION.cff`, and the auto-generated alternatives `citation_apalike.apa` and `citation_bibtex.bib`.

## Licence

This repository is licensed under an [MIT licence](https://github.com/pythonhealthdatascience/stars-reproduce-hernandez-2015/blob/a5ada4714f059d805f769a906bb2f4db0da2da8d/LICENSE).

This is aligned with the original study, who who also licensed their work under the [MIT Licence](https://github.com/ivihernandez/staff-allocation/blob/master/LICENSE).

## Funding

This work is supported by the Medical Research Council [grant number MR/Z503915/1].
