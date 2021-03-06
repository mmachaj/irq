import requests
from prettytable import PrettyTable

class PrintHelper:
    """
    Class with helper methods for printing various CLI outputs in a nice format.

    This class was kept separate from the client class because it doesn't need
    to be concerned with formatting the view of the data it presents.
    """

    def __init__(self, out_stream):
        self.out_stream = out_stream

    def print_cpu_affinity(self, cpu_affinity):
        table = PrettyTable(["IRQ", "CPU Affinity"])
        table.add_row([cpu_affinity['irq_num'], cpu_affinity['cpu_affinity']])

        self.out_stream.write(table.get_string() + "\n")

    def print_irq_info(self, irq_info):
        # num_interrupts_all_cpus = interrupts['totals']['num_interrupts_all_cpus']
        num_interrupts_per_cpu = irq_info['totals']['num_interrupts_per_cpu']

        irqs = irq_info['irqs']
        num_cpus = len(irqs[0]['num_interrupts_per_cpu'])

        cpu_columns = []
        for i in range(0, num_cpus):
            cpu_columns.append("CPU{}".format(i))

        columns = ["IRQ"]  + ["Irq Type", "Device", "CPU Affinity"] + cpu_columns
        table = PrettyTable(columns)
        for irq in irqs:
            columns = []
            columns.append(irq['irq_num'])
            columns.append(irq['device_name'])
            columns.append(irq['irq_type'])
            columns.append(irq['cpu_affinity'])
            columns += irq['num_interrupts_per_cpu']
            table.add_row(columns)

        totals_columns = ["Totals:"]
        totals_columns += ["", "", ""]
        totals_columns += num_interrupts_per_cpu
        table.add_row(totals_columns)

        self.out_stream.write(table.get_string() + "\n")

    def print_interrupts(self, interrupt_totals):
        self.out_stream.write(
            "\nPeriod duration (secs): {}\n\n".format(interrupt_totals['period_duration_seconds']))

        num_interrupts_all_cpus = interrupt_totals['num_interrupts_all_cpus']
        num_interrupts_per_cpu = interrupt_totals['num_interrupts_per_cpu']
        percent_interrupts_per_cpu = interrupt_totals['percent_interrupts_per_cpu']

        table = PrettyTable(["Cpu #", "Total Interrupts", "Percent Interrupts"])
        for i in range(0, len(num_interrupts_per_cpu)):
            table.add_row([
                "{}".format(i),
                num_interrupts_per_cpu[i],
                "{}%".format(round(percent_interrupts_per_cpu[i], 1))
            ])
        table.add_row(["Total:", num_interrupts_all_cpus, ""])

        self.out_stream.write(table.get_string() + "\n")

    def print_interrupts_for_cpu(self, interrupt_totals):
        cpu_num = interrupt_totals['cpu_num']
        period_duration_seconds = interrupt_totals['period_duration_seconds']
        num_interrupts = interrupt_totals['num_interrupts']
        percent_interrupts = interrupt_totals['percent_interrupts']
        num_interrupts_all_cpus = interrupt_totals['num_interrupts_all_cpus']

        table = PrettyTable(["CPU #", cpu_num])
        table.add_row(["# Interrupts", num_interrupts])
        table.add_row(["% Interrupts", "{}%".format(round(percent_interrupts, 1))])
        table.add_row(["# Interrupts All CPUs", num_interrupts_all_cpus])
        table.add_row(["Period Duration (secs)", period_duration_seconds])

        self.out_stream.write(table.get_string() + "\n")

class IrqServiceApi:
    """
    A simplified interface over the HTTP calls made to the REST API.
    """

    def __init__(self, host, port=80):
        self.host = host
        self.port = port

    def do_get(self, path):
        url = "http://{}:{}{}".format(self.host, self.port, path)
        response = requests.get(url)
        return response.json()

    def do_put(self, path, data):
        url = "http://{}:{}{}".format(self.host, self.port, path)
        response = requests.put(url, data=data)
        return response.json()


class IrqClient:
    """
    Provides a high-level interface to the IRQ service.

    The purpose of this class is to provide a simple interface to users that hides
    the details of the underlying API calls.  It parses input parameters and then
    delegates to the API object for the HTTP calls.
    """

    def __init__(self, api):
        self.api = api

    def get_interrupts_for_period(self, period_duration_seconds):
        response_dict = self.api.do_get(
            "/interrupts?period_seconds={}".format(period_duration_seconds))
        return response_dict

    def get_interrupts_for_period_for_cpu(self, cpu_num, period_duration_seconds):
        response_dict = self.api.do_get(
            "/interrupts/cpu/{}?period_seconds={}".format(cpu_num, period_duration_seconds))
        return response_dict

    def get_irq_info(self):
        response_dict = self.api.do_get("/irqs")
        return response_dict

    def get_irq_cpu_affinity(self, irq):
        response_dict = self.api.do_get("/irqs/{}/cpu_affinity".format(irq))
        return response_dict

    def set_irq_cpu_affinity(self, irq, cpu_affinity_mask):
        path = "/irqs/{}/cpu_affinity".format(irq)
        put_data = { 'cpu_affinity_mask': cpu_affinity_mask }
        response = self.api.do_put(path, put_data)
        return response
