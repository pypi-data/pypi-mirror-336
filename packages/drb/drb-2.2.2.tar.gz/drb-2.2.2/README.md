# Data Request Broker
This python module includes data model implementation of DRB (Data Request Broker).
Implementations are provided outside this project and shall be included into the application according to the needs.
See [documentation](https://drb-python.gitlab.io/drb) for details.
# Library usage
Installing ````drb```` with execute the following in a terminal:

    pip install drb
# Notes for developers
## Dev environment setup
The development environment includes all the features required to execute this module unitary test and to deploy it.
When loading the project with pycharm, the tool automatically reads requirements file and sets up the virtual environment.

Installation of a virtual environment is not mandatory but greatly recommended in order to avoid any confusion between system or other projects libraries. Linux package python3-venv shall be installed (```sudo apt install python3-venv``` on ubuntu)

The command line to prepare the virtual environment:
```commandline
python3 -m venv venv
source venv/bin/activate
```
Once successfully run, the command line prompt is updated with the virtual environment name:
```commandline
(venv) $~> _
```
Once the virtual environment installed, the dependencies shall be downloaded:
```commandline
(venv) $~> pip install -r requirements.txt --no-cache-dir
Collecting pip==21.1.2
  Downloading pip-21.1.2-py3-none-any.whl (1.5 MB)
     |████████████████████████████████| 1.5 MB 54 kB/s 
Collecting setuptools==57.0.0
  Downloading setuptools-57.0.0-py3-none-any.whl (821 kB)
     |████████████████████████████████| 821 kB 73 kB/s 
Installing collected packages: pip, setuptools
  Attempting uninstall: pip
    Found existing installation: pip 20.0.2
    Uninstalling pip-20.0.2:
      Successfully uninstalled pip-20.0.2
  Attempting uninstall: setuptools
    Found existing installation: setuptools 44.0.0
    Uninstalling setuptools-44.0.0:
      Successfully uninstalled setuptools-44.0.0
Successfully installed pip-21.1.2 setuptools-57.0.0
```
At this stage the environment is installed.

Other environment virtualization solution such as [Vagrant](http://www.vagrantup.com) are also stable solutions for production.
## Git Contributions
### Contribution process
We are pleased to receive all users contributions. Each contribution shall be documented in english, and code styling shall follow [pep8](https://www.python.org/dev/peps/pep-0008) recommendations.
You can also join the moderators team. Please contact me.

Contribution process is based on gitlab best practice and processes the following schema:

![](docs/modification_process.png)

### How to contribute
Contributor shall work in its own fork of the project and provides its contributions via the merge request process.
The merge request shall be approved and merged by a maintainers. So the step-by-step procedure to contribute is:

- Fork the project,
- Locally clone forked repository.
- Once created, the modification branch could be submitted as merge request in ```Draft``` proposal state.
- Once feature/bug finalized, ```Draft``` flag shall be removed and the assignees/maintainers notified for merge.

Before submission, contributor shall clean up, squash and rebase its commits to be easily inserted as fast-forward into the main branch.
Please read https://chris.beams.io/posts/git-commit as commit writing best practices for this project.
The related issue/bug identifier shall be reported into the commit message, otherwise, the issue shall be commented/closed accordingly.

## Configuration management
The project uses the [```versioneer```](https://github.com/python-versioneer/python-versioneer) tool to manage releases deployement.
Then, the version management and deployment are coupled and can be performed in the same process.
This process secures the deployment process preventing a developer from accidentally deploying and erasing a release version. Versioneer tool checks the local repository then generates a ```dirty``` release when repository is not clean. This process can also be useful when developer needs to deploy snapshots.
Multiple and dirty deployement of versions are forbidden in [pypi.org](https://pypi.org/project/drb) repository, this behavior also secures the version erasing risks.

### Setup the environment
The environment shall be configured to deploy the python library onto Pypi public  repository.
The application used to manage module deployment is ```twine```. This application shall be configured via `````${HOME}/.pypirc````` file as followed:

Alternatively, the private gael's repository can be set (See ```[gael]``` entry.

```properties
[distutils]
index-servers =
  pypi
  drb

[pypi]
username: __token__
password: pypi-XXX

[drb]
repository = https://upload.pypi.org/legacy/
username: __token__
password: pypi-YYY

[gael]
repository: https://repository.gael-systems.com/repository/python-gael/
username: username
password: password
```
The important part is the ```drb``` section which defines the remote repository and credentials or token for the deployment (See https://pypi.org/help/#apitoken for details).

### Perform the release and deployment
The version management is performed automatically with git tags. Setting the version is coupled with the deployment process within the CI/CD process.

To generate a new version, tag the master branch with the expected version and push the new tag version into git:
```commandline
git tag 1.0-rc1
git push origin 1.0-rc1
```
On pushing new tag, a pipeline is automatically executed to control
- code format compliance with [pep8](https://www.python.org/dev/peps/pep-0008/))
- code source security with plugins [bandit](https://bandit.readthedocs.io) and [semgrep](https://semgrep.dev/)
- code unittary tests with python 3.8 and python 3.9
- code coverage computation
- deploy the release into pypi repository.

NB: if the runner is not properly configured to upload distribution to the remote repository, the pipeline executed at tag push time might fail. To perform the distribution manually it shall be possible to run the following command lines:
```commandline
make dist-clean
make dist-deploy
```
See the makefile details in command line section [here after](#command-line).

#### Branching model
In git, thanks to the tag oriented release, the branching model fixes the following rules:
 - All the contributions are merged into the `main` branch.
 - Contribution Merge Requests are merged using fast-forward mode.
 - A dedicated `release-xx` branch can be created for post-release fixes(hotfixes).

### Project Final Releases Stategy

The project release version is based on 3 digits "M.m.f" :
- M: Major version is created when DRB API is modified or interface behavior changed. (i.e. index are used instead of occurrence does not change interface, but greatly change the code behavior) - Usually Major version is created when unitary tests are impacted when they concerns module interface validation.
- m: Minor version is created when new features are introduced without impact on the previous interface: Adding new entries in classes, new classes, add feature in interface method or new feature. (i.e. get_impl is able to manage kwargs dictionary argument to be passed to the sub implementation). Usually minor version is created when unitary tests are added to validate new feature, but old ones stays unchanged.
- f: Fix version is created when a fix or a set of fixes are released. New unitary tests shall be created to ensure non regression of the issue in future changes.

#### Tag management and pre/post releases
Drb project follows the [pep440](https://www.python.org/dev/peps/pep-0440) recommendations for the tag representation. Versions are represented with the couple of (Major, Minor) version numbers for all pre-releases. Modifiers such as alpha (`aN`), beta(`bN`), release candidate(`rcN`), or post release (`.postN`) are possible as followed:
- alpha version: `1.0a1`
- beta version: `1.0b1`
- release candidate version: `1.0rc1`
- Final release: `1.0.0`

Note that (a,b,rc) are based on 2 digits (Major.Minor) whereas Final release are identified on 3 digits as desibed in the [previous chapter](#project-final-releases-stategy): The third digit is used to manage fixes, waiting minor releases.

### Command line
The environment comes with a preconfigured Makefile able to set up and prepare python environment to run tests and coverage. It also provides target to deploy new release manually.

```commandline
make clean
```
Clean-up the environment from cache and lightweight components. It does not removed downloaded dependencies (from venv directory), nor distributions.

```commandline
make dist-clean
```
The `dist-clean` command full cleans the repository as it has been cloned first.
Following the call of `dist-clean` the virtual environment and all the caches will be removed.

```commandline
make test
```
Run the unitary tests.

```commandline
make lint
```
Check if the source code properly follows the pep8 directives. This test is also used in gitlab piplines to accept pushed sources.

```commandline
make coverage
```
Run the test coverage and generates a html report into `htmlcov` directory.

```commandline
make dist
```
Prepare a distribution locally into `dist` directory. When no tag is present on the current commit, or modified files are present into the local directory, the distribution process creates a dirty version to be safety deploy to the repository.

```commandline
make dist-deploy
```
Prepare and deploy a distribution into the gael's remote Pipy repository.
This command is run automatically when pushing a new tag. 

## Limitation
Currently, DRB project is not tested on Windows environment and some issues may appear on Windows systems.

If any troubleshoot occurred with the DRB library, please report us, opening a new issue or accident on the project GitLab page.
