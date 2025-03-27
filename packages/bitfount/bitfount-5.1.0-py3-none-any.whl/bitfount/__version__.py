"""Version information for `setup.py`."""

# ruff: noqa: E501
#   ____  _ _    __                   _
#  | __ )(_) |_ / _| ___  _   _ _ __ | |_
#  |  _ \| | __| |_ / _ \| | | | '_ \| __|
#  | |_) | | |_|  _| (_) | |_| | | | | |_
#  |____/|_|\__|_|  \___/ \__,_|_| |_|\__|
from __future__ import annotations

__author__ = "Bitfount"
__author_email__ = "info@bitfount.com"
__copyright__ = "Copyright 2021 Bitfount Ltd"
__description__ = "Machine Learning and Federated Learning Library."
__title__ = "bitfount"
__url__ = "https://github.com/bitfount/bitfount"
__version__ = "5.1.0"
# YAML versions must be all on one line for the breaking changes script to work
__yaml_versions__ = ["2.0.0", "3.0.0", "4.0.0", "4.0.1", "4.1.0", "5.0.0", "6.0.0", "6.1.0", "6.2.0", "6.2.1", "6.3.0", "6.4.0", "6.5.0", "6.6.0"]  # fmt: off
# major for bitfount breaking changes,
# minor for non-breaking changes,
# patch for plugins versioning
# YAML Version Changes
# - 6.6.0:
#   - Add specifications for datasource and datasplitter (kw)arg dictionaries,
#     to provide tighter specification of these items.
#   - Fix typing of "save path", etc., instances to correctly be specced as string/null
#     rather than types inferred from fields.Function()
#   - Fix Optional[Union[X, Y]] specs to correctly allow None/null
#   - Change Union parsing to export to anyOf instead of oneOf, to better match
#     the expected Marshmallow behaviour.
#   - Fix issue with Union[dict[...],...] fields not being correctly written to
#     the spec if they didn't contain enums.
#   - Fix enum dicts to ensure they are valid JSON Schema components.
#   - Introduce typing for template elements to ensure that those are also adhered to.
# - 6.5.0:
#   - Added NextGenSearchProtocol protocol
#   - Fix incorrect args config for _SimpleCSVAlgorithm
# - 6.4.0:
#   - Added NextGenPatientQuery algorithm
