The python library is named *noofolio*, introduced as part of delivery for the CQF final project.


# Setup

## Set up directly from source code by adding the folder path that contains the library noofolio in the variable PYTHONPATH, e.g.: 
```
PYTHONPATH=c:/git/noofolio
```
wherein we have subfolder *c:/git/noofolio*.

## Install into the python environment via standard setup.py


# Usage

Start with ```import noofolio as pc```

Use High-level API in ```pc.analyse```, e.g.:
```
pc.analyse.asset_recommendations(...)
```

More flexible usage can be directed to sub-modules, e.g.:
```
pc.marketdata.get_md_observable(...)
```

# Design

## APIs
- noofolio.screen(data)
- noofolio.select(candidates)
- noofolio.optimise(portfolio)
- noofolio.monitor(portfolio)

## Flow

monitor (warning?)
  - yes: try in order
    - attempt re-optimise
    - attempt re-select
    - attempt re-screen

optimise (meet risk aversion?)
  - yes: try in order
    - attempt re-select
    - attempt re-screen

select (rating high enough?)
  - yes: try in order
    - attempt re-screen

## Tech Requirement

