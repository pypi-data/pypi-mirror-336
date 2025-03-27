# © Copyright Databand.ai, an IBM Company 2022

from dbnd import dbnd_config
from dbnd._vendor import click
from dbnd_monitor.liveness_probe import MAX_TIME_DIFF_IN_SECONDS, check_monitor_alive


@click.command()
@click.option(
    "--max-time-diff", type=click.INT, help="Maximum time from last liveness file"
)
def airflow_monitor_v2_alive(max_time_diff):
    # we need to load configs,
    # we have multiple get_databand_context().databand_api_client calls
    dbnd_config.load_system_configs()

    check_monitor_alive(max_time_diff=max_time_diff or MAX_TIME_DIFF_IN_SECONDS)


if __name__ == "__main__":
    airflow_monitor_v2_alive()
