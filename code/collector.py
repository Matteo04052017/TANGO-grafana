import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from tango import Database, DeviceProxy, CmdArgType as ArgType, AttrDataFormat

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        g = GaugeMetricFamily("device_attribute", 'Device attribute value', labels=['device', 'attribute', 'label'])
        db = Database()
        count = 0
        error_count = 0
        server_list = db.get_server_list()
        i = 0
        while i < len(server_list):
            class_list = db.get_device_class_list(server_list[i])
            j = 0
            while j < len(class_list):
                try:
                    if not "dserver" in class_list[j]:
                        dev = DeviceProxy(class_list[j])
                        attr_list = dev.attribute_list_query()
                        for attr_info in attr_list:
                            if(attr_info.data_format == AttrDataFormat.SCALAR):
                                attr_value = dev.read_attribute(attr_info.name)
                                g.add_metric([class_list[j], attr_info.name, attr_info.label], attr_value.value)
                                count = count + 1
                except: 
                    error_count += 1
                j += 2
            i += 1
        
        yield g

        c = GaugeMetricFamily("error_count", 'Total number of errors reading the attributes')
        c.add_metric([], error_count)
        yield c

        d = GaugeMetricFamily("attribute_count", 'Total number of attributes')
        d.add_metric([], count)
        yield d


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
