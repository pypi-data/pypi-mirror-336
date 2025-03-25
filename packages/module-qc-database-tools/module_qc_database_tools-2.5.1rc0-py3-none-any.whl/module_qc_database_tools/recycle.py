from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

import pymongo
import requests
from bson.objectid import ObjectId

from module_qc_database_tools.db.local import (
    get_component,
    get_qc_result,
    get_qc_status,
)

log = logging.getLogger(__name__)


def recycle_component(
    db: pymongo.database.Database, serial_number: str, *, localdb_uri: str
) -> (bool, dict[str, (bool, dict[str, (bool, str)])]):
    """
    Recycle all E-SUMMARY across all stages for given component

    Args:
        db (:obj:`pymongo.database.Database`): The database instance for localDB to retrieve information from.
        serial_number (:obj:`str`): the serial number of the component.
        localdb_uri (:obj:`str`): the localDB URI to use for triggering analysis recycling

    Returns:
        success (:obj:`bool`): success or failure for recycling all the E-SUMMARIES
        results (:obj:`dict`): dictionary of status for recycling each stage's E-SUMMARY (see :func:`recycle_e_summary`)
    """
    component, _ = get_component(db, serial_number)
    mod_status = get_qc_status(db, component)

    results = {}
    for stage, qc_results in mod_status["QC_results"].items():
        e_summary_object = qc_results.get("E_SUMMARY", "-1")
        if e_summary_object == "-1":
            log.warning("Stage %s does not have E-SUMMARY, skipping", stage)
            continue

        e_summary = get_qc_result(db, e_summary_object)
        results[stage] = recycle_e_summary(e_summary, localdb_uri=localdb_uri)

    return (all(status for status, _ in results.values()), results)


def recycle_e_summary(
    e_summary: dict[str, Any], *, localdb_uri: str
) -> (bool, dict[str, (bool, str)]):
    """
    Recycle a given e-summary.

    Args:
        e_summary (:obj:`dict`): the e-summary to recycle
        localdb_uri (:obj:`str`): the localDB URI to use for triggering analysis recycling

    Returns:
        success (:obj:`bool`): success or failure for recycling all the tests
        results (:obj:`dict`): dictionary of status, message for recycling each test
    """

    results = {}
    is_complex_analysis = False
    for key, link in e_summary["results"].items():
        if link == 0:
            continue
        if not isinstance(link, str):
            continue

        is_complex_analysis = any(
            test in key
            for test in ["MIN_HEALTH_TEST", "TUNING", "PIXEL_FAILURE_ANALYSIS"]
        )
        results[key] = recycle_analysis(
            link, localdb_uri=localdb_uri, is_complex_analysis=is_complex_analysis
        )

    return (all(status for status, _ in results.values()), results)


def recycle_analysis(
    test_run_id: str | ObjectId, *, localdb_uri: str, is_complex_analysis: bool = False
) -> (bool, str):
    """
    Recycle a given analysis using it's specific identifier.

    Args:
        test_run_id (:obj:`str` or :obj:`bson.objectid.ObjectId`): the identifier of the test run to recycle
        localdb_uri (:obj:`str`): the localDB URI to use for triggering analysis recycling
        is_complex_analysis (:obj:`bool`): whether the analysis to recycle is complex or not

    Returns:
        status (:obj:`bool`): whether the analysis was recycled successfully
        message (:obj:`str`): message providing context for status

    """
    result = requests.post(
        urljoin(
            localdb_uri,
            "recycle_complex_analysis" if is_complex_analysis else "recycle_analysis",
        ),
        json={"test_run_id": str(test_run_id)},
        timeout=120,
        headers={"Accept": "application/json"},
    )
    status = result.status_code == 200
    try:
        content = result.json()["message"]
    except KeyError:
        content = result.json()
    except ValueError:
        content = result.content

    return (status, "Ok" if status else content)
