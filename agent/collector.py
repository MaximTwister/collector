from typing import List

import psutil

from config import AgentConfig
from metric import Metric


class AgentCollector(AgentConfig):

    def __init__(self, *args, **kwargs):
        self.metrics: List[Metric] = []
        super().__init__(*args, **kwargs)

    def collect_cpu_metrics(self):
        """
        descr: represents the CPU time has spent in the given mode
        units: seconds
        :return: None
        """

        if not self.cpu:
            return False

        units = "seconds"
        cpu_times = psutil.cpu_times()

        data = [
            ("cpu_time_user", cpu_times.user, units),
            ("cpu_time_system", cpu_times.system, units),
            ("cpu_time_idle", cpu_times.idle, units),
        ]

        for metric in data:
            self.metrics.append(Metric(*metric))

    def collect_memory_metrics(self):
        """
        descr: return statistics about system memory usage
        units: bytes
        :return: None
        """

        units = "bytes"
        virtual_memory = psutil.virtual_memory()

        data = [
            ("virt_mem_total", virtual_memory.total, units),
            ("virt_mem_available", virtual_memory.available, units),
            ("virt_mem_used", virtual_memory.used, units),
            ("virt_mem_free", virtual_memory.free, units),
        ]

        for metric in data:
            self.metrics.append(Metric(*metric))


ac = AgentCollector(configuration_file="./configs/agent.yaml")
ac.collect_cpu_metrics()
ac.collect_memory_metrics()
