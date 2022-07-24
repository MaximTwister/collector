import argparse

import requests
from requests.exceptions import ConnectionError
from apscheduler.schedulers.blocking import BlockingScheduler

from collector import AgentCollector

parser = argparse.ArgumentParser(description="Agent for local metrics collection")
parser.add_argument("--ip", dest="ip", required=True)
parser.add_argument("--port", dest="port", required=True)
parser.add_argument("--config", dest="config", required=True)

parser_args = parser.parse_args()

if not parser_args.port.isdigit() or int(parser_args.port) not in range(65536):
    parser.error("port must be integer from 0 to 65535")

metrics_endpoint = f"http://{parser_args.ip}:{parser_args.port}/api/v1/metrics"


class Agent(AgentCollector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def collect(self):
        self.collect_cpu_metrics()
        self.collect_memory_metrics()

    def send_metrics(self):
        while self.metrics_models:
            metric_model = self.metrics_models.pop()
            data = metric_model.dict()
            print(f"[debug][{type(data)}] send: {data}")

            try:
                res = requests.post(metrics_endpoint, json=data)
            except ConnectionError as e:
                print(f"[err] connection error: {e}")
                continue

            if res.ok:
                print(f"[debug] response: {res.json()}")
            else:
                print(f"[err] bad response: {res}")

    def job(self):
        print(f"[info] Agent has been created")
        self.collect()
        self.send_metrics()


if __name__ == "__main__":
    agent = Agent(configuration_file=parser_args.config)
    scheduler = BlockingScheduler(standalone=True)
    scheduler.add_job(
        func=agent.job,
        trigger="interval",
        seconds=agent.interval,
        id="agent_job",
    )
    scheduler.start()
