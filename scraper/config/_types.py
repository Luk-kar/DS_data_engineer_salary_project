'''
This module provides type aliases for configuration values for the scraper.
'''

from typing import Any, Annotated, Literal, TypedDict
from annotated_types import Gt

JobDefault = str
JobSimilar = list[str]
JobTitles = TypedDict('JobTitles', {'default': JobDefault,
                                    'similar': JobSimilar})
JobNumber = Annotated[int, Gt(0)]
Url = dict[str, str]
DriverPath = str
DebugMode = bool
NA_value = Literal[-1]
OutputPath = TypedDict('OutputPath', {'main': str, 'raw': str, 'clean': str})
Config = TypedDict('Config', {'jobs_titles': JobTitles, 'jobs_number': JobNumber, 'url': Url,
                              'driver_path': DriverPath, 'debug_mode': DebugMode, "NA_value": NA_value,
                              'output_path': OutputPath}
                   )
