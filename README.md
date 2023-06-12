# ml-template
Template repo for Machine Learning projects

## Conventions

### PEP8
We stick to [PEP8](https://www.python.org/dev/peps/pep-0008/) in general. We use [numpy style](https://numpydoc.readthedocs.io/en/latest/format.html) for docstrings.

### Line length
Docstrings - strict limit of 72 characters. Code - limit of 79 characetrs is recomended but not strict.


## Experiment monitoring
We have a nice dedicated tool for monitoring of the experiments: neptune.ai. It has a well documented API and we can use it directly without writing any wrappers around it.


## Environment setup

### Rational
We recommend using `conda` as an environment manager only, `pip` as the package installer, and `poetry` as the dependency manager. See this [source](https://ealizadeh.com/blog/guide-to-python-env-pkg-dependency-using-conda-poetry) for more details.

### Steps

1. **Skip** Modify `conda.yaml` and commit it. Rename also the `foo` dir ;) 

```yaml
name: foo  # <- Replace foo with the real project name

channels:
  - conda-forge
  - default

dependencies:
  - python=3.10  # <- Replace 3.10 if needed

```

2. Create virtual environment

```shell
conda env create -f conda.yaml

conda activate <project name>
```

3. Install `poetry` if you don't have it yet.

```shell
curl -sSL https://install.python-poetry.org | python -

```
You may need to update your path as suggested by the installer.


4. **Skip** Initialize poetry project:
```shell
poetry init
```
and follow answering the questions. When asked about python, change default Compatible Python versions from "^3.10" to "~3.10".

At this stage add these basic packages: 
* `scikit-learn`
* `streamlit`
* `python-dotenv`

You can add more packages later with `poetry add`. Commit and push `pyproject.toml` file that has been just created.

5. Install dependencies from `pyproject.toml` by
```shell
poetry install
```
It can take a few minutes.

> Side remark: poetry will use conda environment that you created and activated, see [doc](https://python-poetry.org/docs/managing-environments/).
> So next time you want to run a script, you can either use `poetry run ...` or much faster way: activate conda env and use `python ...` directly.

> Optional: you can commit `poetry.lock` file too if you are OK with solving its conflicts later on.

6. Secrets

Make a copy of `.env.example` and save it as `.env`. Put your secrets there. Never commit it (it should be ignored by git).


### Summary
That's it. If you are a second developer on the project and someone already modified `conda.yaml` and done `poetry init` you should skip steps 1 and 4.


## Git rules
0. Rebase your branch on `master` before starting PR.
1. Write professional git messages:
- Use present simple imperative in git commits. 
- Start with capital letter. 
- Don't end with period. 
- Ideally, follow [these seven rules](https://chris.beams.io/posts/git-commit/#seven-rules).

Good example:
```shell
Add DataLoader
```

2. Remove merged branches on remote (github proposes that after merge)
3. Discuss in team merging strategy - with squash or without?
4. Never allow for commented out code in PR.


## Running the training
Add steps to execute the training.
```shell
python foo/train.py
```

## Running a demo app
```shell
streamlit run foo/app.py
```


## Library decision record
Explain in 1 sentence the key factors that made you chose the main libraries for the project.

E.g.: We have chosen pytorch over TF, because it allows for easier export to ONNX, which is necessary for the deployment.


## Data Sources
Describe shortly sources of data. For example:

| source | #samples | size | location | remarks |
| --- | --- | --- | --- | --- |
Initial photos | 2500 | 2.1GB | s3://foo/bar/ | Bad quality |

Put whatever you want in this section, make it the single source of truth regrading the data.
