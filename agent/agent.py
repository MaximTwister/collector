import argparse

import requests
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

    def create_meta_fields(self):
        return {
            "source_name": self.source_name,
            "hostname": self.hostname,
            "host_id": self.host_identificator,
        }

    def send_metrics(self):
        while self.metrics:
            metric = self.metrics.pop()
            metric.meta = self.create_meta_fields()

            data = metric.to_json()
            res = requests.post(metrics_endpoint, json=data)

            if res.ok:
                print(f"[debug] response {res.json()}")
            else:
                print(f"[debug] bad response {res}")

    def job(self):
        self.collect()
        self.send_metrics()


if __name__ == "__main__":
    agent = Agent(configuration_file=parser_args.config)
    scheduler = BlockingScheduler(standalone=True)
    scheduler.add_job(agent.job, "interval", seconds=agent.interval, id="agent_job")
    scheduler.start()
