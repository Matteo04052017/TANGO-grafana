import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from tango import Database, DeviceProxy, CmdArgType as ArgType, AttrDataFormat

class CustomCollector(object):
    def __init__(self):
        self.db = Database()
        pass

    def collect(self):
        g = GaugeMetricFamily("device_attribute", 'Device attribute value', labels=['device', 'name', 'label', 'string_value'])
        total_count = 0
        read_count = 0
        error_count = 0
        scalar_attribute = 0
        not_managed_attribute_count = 0
        multidimension_attribute = 0
        server_list = self.db.get_server_list()
        i = 0
        while i < len(server_list):
            class_list = self.db.get_device_class_list(server_list[i])
            j = 0
            while j < len(class_list):
                try:
                    dev = DeviceProxy(class_list[j])
                    attr_list = dev.attribute_list_query()
                    for attr_info in attr_list:
                        total_count += 1
                        # {0: tango._tango.CmdArgType.DevVoid,
                        #  1: tango._tango.CmdArgType.DevBoolean,*
                        #  2: tango._tango.CmdArgType.DevShort,*
                        #  3: tango._tango.CmdArgType.DevLong,*
                        #  4: tango._tango.CmdArgType.DevFloat,*
                        #  5: tango._tango.CmdArgType.DevDouble,*
                        #  6: tango._tango.CmdArgType.DevUShort,*
                        #  7: tango._tango.CmdArgType.DevULong,*
                        #  8: tango._tango.CmdArgType.DevString,
                        #  9: tango._tango.CmdArgType.DevVarCharArray,
                        #  10: tango._tango.CmdArgType.DevVarShortArray,
                        #  11: tango._tango.CmdArgType.DevVarLongArray,
                        #  12: tango._tango.CmdArgType.DevVarFloatArray,
                        #  13: tango._tango.CmdArgType.DevVarDoubleArray,
                        #  14: tango._tango.CmdArgType.DevVarUShortArray,
                        #  15: tango._tango.CmdArgType.DevVarULongArray,
                        #  16: tango._tango.CmdArgType.DevVarStringArray,
                        #  17: tango._tango.CmdArgType.DevVarLongStringArray,
                        #  18: tango._tango.CmdArgType.DevVarDoubleStringArray,
                        #  19: tango._tango.CmdArgType.DevState,
                        #  20: tango._tango.CmdArgType.ConstDevString,
                        #  21: tango._tango.CmdArgType.DevVarBooleanArray,
                        #  22: tango._tango.CmdArgType.DevUChar,
                        #  23: tango._tango.CmdArgType.DevLong64,*
                        #  24: tango._tango.CmdArgType.DevULong64,*
                        #  25: tango._tango.CmdArgType.DevVarLong64Array,
                        #  26: tango._tango.CmdArgType.DevVarULong64Array,
                        #  27: tango._tango.CmdArgType.DevInt,*
                        #  28: tango._tango.CmdArgType.DevEncoded, *****????????
                        #  29: tango._tango.CmdArgType.DevEnum, *****????????
                        #  30: tango._tango.CmdArgType.DevPipeBlob, *****????????
                        #  31: tango._tango.CmdArgType.DevVarStateArray}
                        if(attr_info.data_format == AttrDataFormat.SCALAR):
                            if(attr_info.data_type == ArgType.DevShort or attr_info.data_type == ArgType.DevLong or
                                attr_info.data_type == ArgType.DevUShort or attr_info.data_type == ArgType.DevULong or
                                attr_info.data_type == ArgType.DevLong64 or attr_info.data_type == ArgType.DevULong64 or
                                attr_info.data_type == ArgType.DevInt or attr_info.data_type == ArgType.DevFloat or 
                                attr_info.data_type == ArgType.DevDouble):
                                    attr_value = dev.read_attribute(attr_info.name)
                                    g.add_metric([class_list[j], attr_info.name, attr_info.label, ''], float(attr_value.value))
                                    read_count = read_count + 1
                            elif(attr_info.data_type == ArgType.DevBoolean):
                                attr_value = dev.read_attribute(attr_info.name)
                                g.add_metric([class_list[j], attr_info.name, attr_info.label, ''], int(attr_value.value))
                                read_count = read_count + 1
                            elif(attr_info.data_type == ArgType.DevString):
                                attr_value = dev.read_attribute(attr_info.name)
                                g.add_metric([class_list[j], attr_info.name, attr_info.label, str(attr_value.value)], 1)
                                read_count = read_count + 1
                            elif(attr_info.data_type == ArgType.DevEnum):
                                attr_value = dev.read_attribute(attr_info.name)
                                g.add_metric([class_list[j], attr_info.name, attr_info.label, str(attr_value.value)], int(attr_value.value))
                                read_count = read_count + 1
                            elif(attr_info.data_type == ArgType.DevState):
                                attr_value = dev.read_attribute(attr_info.name)
                                g.add_metric([class_list[j], attr_info.name, attr_info.label, str(attr_value.value)], int(attr_value.value))
                                read_count = read_count + 1
                            else:
                                not_managed_attribute_count += 1
                                print("*******NOT MANAGED**********")
                                print(attr_info)
                                print("****************************")
                        else:
                            multidimension_attribute += 1
                except Exception as e: 
                    print ("Could not connect to the '"+class_list[j]+"' DeviceProxy.\r\n")
                    print (e)
                    error_count += 1
                j += 2
            i += 1
        
        yield g

        c = GaugeMetricFamily("error_count", 'Total number of errors reading the attributes')
        c.add_metric([], error_count)
        yield c

        d = GaugeMetricFamily("total_attribute_count", 'Total number of attributes')
        d.add_metric([], total_count)
        yield d

        e = GaugeMetricFamily("attribute_count", 'Total number of read attributes')
        e.add_metric([], read_count)
        yield e

        f = GaugeMetricFamily("multidimension_attribute_count", 'Total number of multi dimension attributes')
        f.add_metric([], multidimension_attribute)
        yield f

        g = GaugeMetricFamily("not_managed_attribute_count", 'Total number of not managed attributes')
        g.add_metric([], not_managed_attribute_count)
        yield g


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
