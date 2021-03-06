from flask.ext.restful import fields

#------------------------------------------------------------------------------
# Marshaller mappings
#------------------------------------------------------------------------------
irq_fields = {
    'irq_num': fields.String,
    'irq_type': fields.String,
    'device_name': fields.String,
    'cpu_affinity': fields.String,
    'num_interrupts_per_cpu': fields.List(fields.Integer)
}

interrupt_totals_fields = {
    'num_interrupts_all_cpus': fields.Integer,
    'num_interrupts_per_cpu': fields.List(fields.Integer)
}

interrupts_for_period_fields = {
    'num_interrupts_per_cpu': fields.List(fields.Integer),
    'percent_interrupts_per_cpu': fields.List(fields.Float),
    'num_interrupts_all_cpus': fields.Integer,
    'period_duration_seconds': fields.Integer,
    'num_cpus': fields.Integer
}

interrupts_for_period_for_cpu_fields = {
    'cpu_num': fields.String,
    'num_interrupts': fields.Integer,
    'percent_interrupts': fields.Float,
    'num_interrupts_all_cpus': fields.Integer,
    'period_duration_seconds': fields.Integer,
    'num_cpus': fields.Integer
}

irq_info_fields = {
    'totals': fields.Nested(interrupt_totals_fields),
    'irqs': fields.List(fields.Nested(irq_fields), attribute='irqs')
}

irq_cpu_affinity_fields = {
    'irq_num': fields.String,
    'cpu_affinity': fields.String
}

#------------------------------------------------------------------------------
# Models
#------------------------------------------------------------------------------
class CpuAffinityInfo:
    """
    Represents a current pairing of IRQ to a CPU
    """

    def __init__(self, irq_num, cpu_affinity):
        self.irq_num = irq_num
        self.cpu_affinity = cpu_affinity

class InterruptTotals:
    """
    A reprentation of how interrupts are totalled across all CPUs & individual CPUs
    """

    def __init__(self, num_interrupts_all_cpus, num_interrupts_per_cpu):
        self.num_interrupts_all_cpus = num_interrupts_all_cpus
        self.num_interrupts_per_cpu = num_interrupts_per_cpu

class InterruptTotalsForPeriodForCpu:
    """
    Represents the # of interrupts for a specific CPU over a specific time period (seconds)
    """

    def __init__(self, cpu_num, num_interrupts, percent_interrupts, period_duration_seconds, num_cpus, num_interrupts_all_cpus) :
        self.cpu_num = cpu_num
        self.num_interrupts = num_interrupts
        self.percent_interrupts = percent_interrupts
        self.period_duration_seconds = period_duration_seconds
        self.num_cpus = num_cpus
        self.num_interrupts_all_cpus = num_interrupts_all_cpus

class InterruptTotalsForPeriod:
    """
    Represents the # of interrupts for all CPUs over a specific time period (seconds)
    """

    def __init__(self, num_interrupts_per_cpu, period_duration_seconds, num_cpus) :
        self.num_interrupts_per_cpu = num_interrupts_per_cpu
        self.period_duration_seconds = period_duration_seconds
        self.num_cpus = num_cpus

        self.num_interrupts_all_cpus = sum(num_interrupts_per_cpu)
        self.percent_interrupts_per_cpu = [100.0*(cpu/self.num_interrupts_all_cpus) for cpu in num_interrupts_per_cpu]

class Irq:
    """
    Represents info about an IRQ including its current CPU affinity mask
    """

    def __init__(self, irq_num, irq_type, device_name, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.irq_type = irq_type
        self.device_name = device_name
        self.num_interrupts_per_cpu = num_interrupts_per_cpu
        self.cpu_affinity = None

class IrqInfo:
    """
    Represents info about all the IRQs in a system and interrupt totals for those IRQs
    """

    def __init__(self, irqs, totals):
        self.irqs = irqs
        self.totals = totals
