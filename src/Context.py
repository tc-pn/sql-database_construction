"""
This module is used to define a Context class that will be used 
1. to monitor the data of interest,
2. create a logging service Logging that will motinor the state of the pipeline and which step is being executed
3. register failed tasks and rejected rows from validation processes by using a Rejected custom class
"""
from typing import Any

from dataclasses import dataclass, field

@dataclass
class Context:
    data : Any = None # initialisé à None, puis devient un pd.DataFrame
    metrics : dict[str, Any] = field(default_factory=dict)
    logs : list[dict[str, Any]] = field(default_factory=list)
    rejected : list[dict[str, Any]] = field(default_factory=list)
    metadata : dict[str, Any] = field(default_factory=dict)

@dataclass
class Rejected:
    step : str
    error : str
    record : dict[str, Any] = field(default_factory=dict)

    