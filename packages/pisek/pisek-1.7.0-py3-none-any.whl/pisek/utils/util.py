# pisek  - Tool for developing tasks for programming competitions.
#
# Copyright (c)   2019 - 2022 Václav Volhejn <vaclav.volhejn@gmail.com>
# Copyright (c)   2019 - 2022 Jiří Beneš <mail@jiribenes.com>
# Copyright (c)   2020 - 2022 Michal Töpfer <michal.topfer@gmail.com>
# Copyright (c)   2022        Jiří Kalvoda <jirikalvoda@kam.mff.cuni.cz>
# Copyright (c)   2023        Daniel Skýpala <daniel@honza.info>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import shutil
from typing import Optional

from pisek.jobs.cache import CACHE_CONTENT_FILE
from pisek.config.task_config import load_config
from pisek.utils.paths import BUILD_DIR, TESTS_DIR, INTERNALS_DIR


def rm_f(fn):
    try:
        os.unlink(fn)
    except FileNotFoundError:
        pass


def _clean_subdirs(task_dir: str, subdirs: list[str]) -> None:
    for subdir in subdirs:
        full = os.path.join(task_dir, subdir)
        try:
            shutil.rmtree(full)
        except FileNotFoundError:
            pass


def is_task_dir(task_dir: str, pisek_directory: Optional[str]) -> bool:
    # XXX: Safeguard, raises an exception if task_dir isn't really a task
    # directory
    config = load_config(
        task_dir, suppress_warnings=True, pisek_directory=pisek_directory
    )
    return config is not None


def clean_task_dir(task_dir: str, pisek_directory: Optional[str]) -> bool:
    rm_f(os.path.join(task_dir, CACHE_CONTENT_FILE))
    _clean_subdirs(task_dir, [BUILD_DIR, TESTS_DIR, INTERNALS_DIR])
    return True


def clean_non_relevant_files(accessed_files: set[str]) -> None:
    accessed_dirs = {os.path.dirname(file) for file in accessed_files}
    for root, _, files in os.walk(TESTS_DIR):
        for file in files:
            path = os.path.join(root, file)
            if root in accessed_dirs and path not in accessed_files:
                os.remove(path)
