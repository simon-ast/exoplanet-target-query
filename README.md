# Exoplanet Target Query

With this, somewhat abstracted, idea, I want to make an effort in trying to
unify queries of exoplanet system and body names. The impetus for this comes 
from the problems I have had with comparing lists of exoplanets (e.g. a target
list from JWST observational cycle 1, and the preliminary Ariel Tier 2 target 
list).

The actual routine is rather small: It takes the input of a file of query 
target names (for an example, see `test_targets.txt`), and queries 
[SIMBAD](http://simbad.cds.unistra.fr/simbad/) 
for the common name of the object. The whole process is based on the 
[astroquery.simbad](https://astroquery.readthedocs.io/en/latest/simbad/simbad.html) 
package.

The routine returns a csv-file containing the query-results. Importantly, should
a query fail (i.e. the input name not be recognised), then that case is logged
as an `N/A` entry in the result-file. The routine also creates a log (`simbad_query.log`) with some information from
the execution of the routine (might be useful).

## Example
Below is an example of the log-file output, showing that one (1) object
could not be queried correctly.
```
INFO:main: Started programme

INFO:read_targets: From file test_targets.txt querying the list
['NGTS-10b' 'WASP39b' 'wasp39b' 'wasp 39 b' 'wasp-39 b' 'wasp39B'
 'WASP 101 b' 'planet not']

INFO:make_query: Queried fields are ['main_id', 'typed_id']

INFO:query_names: Querying 8 objects...
INFO:query_names: Failed to find 1 object(s):
['planet not']

INFO:main: Completed
```
The corresponding csv-file looks like this:
```
SIMBAD,INPUT
NGTS-10b,NGTS-10b
WASP-39b,WASP39b
WASP-39b,wasp39b
WASP-39b,wasp 39 b
WASP-39b,wasp-39 b
WASP-39b,wasp39B
CPD-23  1329b,WASP 101 b
N/A,planet not
```
This is about as simple as it gets, but it should be easy enough to use
this result-table in other applications.