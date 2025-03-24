# Physics Informed Preconditioners

## Introduction

Pipre, short for Physics Informed Preconditioners, is a large-scale linear equation solver package. It supports distributed heterogeneous parallel computing (MPI+CPU/GPU/DCU/...) and provides physics-informed preconditioners for solvers, especially physics-informed AMG preconditioners. It is dedicated to stably and efficiently solving large-scale linear algebraic equations derived from the discretization of mathematical and physical models.

## Install

``` bash
$ pip install pipre
```

## Usage
use the following command to get the help message:
```bash
$ python -m pipre help
```
copy the example out
```
$ cp -r path_to_pipre/examples .
```
then run the example:
```bash
$ python solver.py thermal1.mtx thermal1_b.mtx solver.json
```

The following python script shows the above solver.py.
read matrix A and vector b from MatrixMarket files,
using CUDA to solve Ax=b.
```python
# solver.py
import pipre
import sys, re, os
#import json
import commentjson as json

fnA = sys.argv[1]
fnb = sys.argv[2]
config = sys.argv[3]

params = json.load(open(config))

A = pipre.ParCSRMatrix()
A.loadFromFile(fnA)
b = pipre.ParMatrix()
b.loadFromFile(fnb)
if b.getSize() == 0:
    b.resize(A.getRows(), 1)
    b.fill(1)

# transfer the matrix and vector to gpu 0.
dev = pipre.Device("cuda:0")
A = A.toDevice(dev)
b = b.toDevice(dev)

# use gpu 0 to finish the computation.
precond = pipre.createPrecond(params["preconditioner"])
precond.setup(A)
solver = pipre.createSolver(params["solver"])
solver.setup(A)

out = solver.solve(precond, A, b)
```

## Solvers and Preconditioners
use
```bash
$ python -m pipre info
```
to show the builtin solvers, preconditioners, smoothers, level_transfers.


## Compatibility
- ### OS version
Now support Linux, Ubuntu/Federa/... will be OK. 
Windows version will be available later.

- ### PYTHON version
the python version is >=3.8. 

- ### GPU/CUDA version
If you want to use CUDA, ensure that 
CUDA Version >= 12.4. 

- ### DCU version
please contact us to compile the specified version.

- ### DISTRIBUTED version
MPI support is on going.


## License

This software is free software distributed under the Lesser General Public 
License or LGPL, version 3.0 or any later versions. This software distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even 
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with PIPRE. If not, see <http://www.gnu.org/licenses/>.

This software depends on GLOG, AMGCL, their license files are located in the package.
