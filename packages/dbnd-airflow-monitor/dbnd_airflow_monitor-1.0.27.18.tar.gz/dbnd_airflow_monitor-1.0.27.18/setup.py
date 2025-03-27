# © Copyright Databand.ai, an IBM Company 2022

from os import path

import setuptools

from setuptools.config import read_configuration


BASE_PATH = path.dirname(__file__)
CFG_PATH = path.join(BASE_PATH, "setup.cfg")

config = read_configuration(CFG_PATH)
version = config["metadata"]["version"]

setuptools.setup(
    name="dbnd-airflow-monitor",
    package_dir={"": "src"},
    install_requires=["dbnd==" + version, "dbnd-monitor==" + version, "setuptools"],
    extras_require={
        "tests": ["pytest", "mock", "sh"],
        "composer": [
            "PyJWT==2.4.0",
            "cryptography==37.0.2",
            "google-auth==1.10.0",
            "requests==2.22.0",
            "requests_toolbelt==0.9.1",
            "tzlocal>=1.5.1",
        ],
    },
    entry_points={
        # TODO: deprecate this one, is used by monitor DAG
        "console_scripts": [
            "dbnd-airflow-monitor = airflow_monitor.multiserver.cmd_multiserver:airflow_monitor_v2",
            "dbnd-airflow-monitor-alive = airflow_monitor.multiserver.cmd_liveness_probe:airflow_monitor_v2_alive",
        ]
    },
)
