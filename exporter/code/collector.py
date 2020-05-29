import time
import argparse
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from tango import Database, DeviceProxy, CmdArgType as ArgType, AttrDataFormat

class CustomCollector(object):
    def __init__(self):
        self.db = Database()
        self.replicas=1
        self.replica_id=0
        pass

    def add_to_metric(self, dev, attr_info, metric):
        if(attr_info.data_type == ArgType.DevShort or attr_info.data_type == ArgType.DevLong or
            attr_info.data_type == ArgType.DevUShort or attr_info.data_type == ArgType.DevULong or
            attr_info.data_type == ArgType.DevLong64 or attr_info.data_type == ArgType.DevULong64 or
            attr_info.data_type == ArgType.DevInt or attr_info.data_type == ArgType.DevFloat or 
            attr_info.data_type == ArgType.DevDouble):
                attr_value = dev.read_attribute(attr_info.name)
                metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, '', 'float', str(attr_value.dim_x), str(attr_value.dim_y), '0', '0'], float(attr_value.value))
                return 1
        elif(attr_info.data_type == ArgType.DevBoolean):
            attr_value = dev.read_attribute(attr_info.name)
            metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, '','bool', str(attr_value.dim_x), str(attr_value.dim_y), '0', '0'], int(attr_value.value))
            return 1
        elif(attr_info.data_type == ArgType.DevString):
            attr_value = dev.read_attribute(attr_info.name)
            metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value),'string', str(attr_value.dim_x), str(attr_value.dim_y), '0', '0'], 1)
            return 1
        elif(attr_info.data_type == ArgType.DevEnum):
            attr_config = dev.get_attribute_config(attr_info.name)
            attr_value = dev.read_attribute(attr_info.name)
            metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_config.enum_labels[attr_value.value]),'enum', str(attr_value.dim_x), str(attr_value.dim_y), '0', '0'], int(attr_value.value))
            return 1
        elif(attr_info.data_type == ArgType.DevState):
            attr_value = dev.read_attribute(attr_info.name)
            metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value),'state', str(attr_value.dim_x), str(attr_value.dim_y), '0', '0'], int(attr_value.value))
            return 1
        else:
            return 0

    def add_to_metric_spectrum(self, dev, attr_info, metric):
        attr_value = dev.read_attribute(attr_info.name)
        for x in range(int(attr_value.dim_x)):
            if(attr_info.data_type == ArgType.DevShort or attr_info.data_type == ArgType.DevLong or
                attr_info.data_type == ArgType.DevUShort or attr_info.data_type == ArgType.DevULong or
                attr_info.data_type == ArgType.DevLong64 or attr_info.data_type == ArgType.DevULong64 or
                attr_info.data_type == ArgType.DevInt or attr_info.data_type == ArgType.DevFloat or 
                attr_info.data_type == ArgType.DevDouble):
                    metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, '', 'float', str(attr_value.dim_x), str(attr_value.dim_y), str(x), '0'], float(attr_value.value[x]))
            elif(attr_info.data_type == ArgType.DevBoolean):
                metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, '','bool', str(attr_value.dim_x), str(attr_value.dim_y), str(x), '0'], int(attr_value.value[x]))
            elif(attr_info.data_type == ArgType.DevString):
                metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value[x]),'string', str(attr_value.dim_x), str(attr_value.dim_y), str(x), '0'], 1)
            elif(attr_info.data_type == ArgType.DevEnum):
                metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value[x]),'enum', str(attr_value.dim_x), str(attr_value.dim_y), str(x), '0'], int(attr_value.value[x]))
            elif(attr_info.data_type == ArgType.DevState):
                metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value[x]),'state', str(attr_value.dim_x), str(attr_value.dim_y), str(x), '0'], int(attr_value.value[x]))
            else:
                pass
        return 1

    def add_to_metric_image(self, dev, attr_info, metric):
        attr_value = dev.read_attribute(attr_info.name)
        for y in range(int(attr_value.dim_y)): 
            for x in range(int(attr_value.dim_x)):
                if(attr_info.data_type == ArgType.DevShort or attr_info.data_type == ArgType.DevLong or
                    attr_info.data_type == ArgType.DevUShort or attr_info.data_type == ArgType.DevULong or
                    attr_info.data_type == ArgType.DevLong64 or attr_info.data_type == ArgType.DevULong64 or
                    attr_info.data_type == ArgType.DevInt or attr_info.data_type == ArgType.DevFloat or 
                    attr_info.data_type == ArgType.DevDouble):
                        metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, '', 'float', str(attr_value.dim_x), str(attr_value.dim_y), str(x), str(y)], float(attr_value.value[y][x]))
                elif(attr_info.data_type == ArgType.DevBoolean):
                    metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, '','bool', str(attr_value.dim_x), str(attr_value.dim_y), str(x), str(y)], int(attr_value.value[y][x]))
                elif(attr_info.data_type == ArgType.DevString):
                    metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value[y][x]),'string', str(attr_value.dim_x), str(attr_value.dim_y), str(x), str(y)], 1)
                elif(attr_info.data_type == ArgType.DevEnum):
                    metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value[y][x]),'enum', str(attr_value.dim_x), str(attr_value.dim_y), str(x), str(y)], int(attr_value.value[y][x]))
                elif(attr_info.data_type == ArgType.DevState):
                    metric.add_metric([dev.dev_name(), attr_info.name, attr_info.label, str(attr_value.value[y][x]),'state', str(attr_value.dim_x), str(attr_value.dim_y), str(x), str(y)], int(attr_value.value[y][x]))
                else:
                    pass
        return 1

    def collect(self):
        attribute_metrics = GaugeMetricFamily("device_attribute", 'Device attribute value', labels=['device', 'name', 'label', 'str_value', 'type', 'dim_x', 'dim_y', 'x', 'y'])
        total_count = 0
        read_count = 0
        error_count = 0
        error_attr_count = 0
        scalar_count = 0
        spectrum_count = 0
        image_count = 0
        not_managed_attribute_count = 0
        try:
            server_list = self.db.get_server_list()
        except:
            try:
                self.db = Database()
            except:
                return

        count = len(server_list) / self.replicas # 15,8
        i = int(count * self.replica_id) # 0 15,8 31,6 47,4 63,2 -> 0 15 31 47 63
        count = int(count) + i # 15 31 47 63 
        if(self.replicas-1 == self.replica_id):
            count = len(server_list) # 79
        #print("i=" + str(i) +",count="+str(count))
        while i < count:
            # https://pytango.readthedocs.io/en/stable/database.html#tango.Database.get_device_class_list
            class_list = self.db.get_device_class_list(server_list[i])
            j = 0
            while j < len(class_list):
                try:
                    if "dserver" in class_list[j]:
                        j += 2
                        continue
                    dev = DeviceProxy(class_list[j])
                    #print(class_list[j])
                    dev.set_timeout_millis(10)
                    attr_list = dev.attribute_list_query()
                    for attr_info in attr_list:
                        try:
                            #print("       " +attr_info.name)

                            total_count += 1
                            #  1: tango._tango.CmdArgType.DevBoolean,
                            #  2: tango._tango.CmdArgType.DevShort,
                            #  3: tango._tango.CmdArgType.DevLong,
                            #  4: tango._tango.CmdArgType.DevFloat,
                            #  5: tango._tango.CmdArgType.DevDouble,
                            #  6: tango._tango.CmdArgType.DevUShort,
                            #  7: tango._tango.CmdArgType.DevULong,
                            #  8: tango._tango.CmdArgType.DevString, 
                            #  19: tango._tango.CmdArgType.DevState,
                            #  23: tango._tango.CmdArgType.DevLong64,
                            #  24: tango._tango.CmdArgType.DevULong64,
                            #  27: tango._tango.CmdArgType.DevInt,
                            #  29: tango._tango.CmdArgType.DevEnum, 
                            if(attr_info.data_format == AttrDataFormat.SCALAR):
                                res = self.add_to_metric(dev, attr_info, attribute_metrics)
                                if(res > 0):
                                    read_count = read_count + res
                                    scalar_count += 1
                                else:
                                    # {0: tango._tango.CmdArgType.DevVoid,
                                    #  28: tango._tango.CmdArgType.DevEncoded, 
                                    #  30: tango._tango.CmdArgType.DevPipeBlob,
                                    #  22: tango._tango.CmdArgType.DevUChar,
                                    #  20: tango._tango.CmdArgType.ConstDevString,
                                    not_managed_attribute_count += 1
                                    #print("*******NOT MANAGED: "+attr_info.name)
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
                            #  21: tango._tango.CmdArgType.DevVarBooleanArray,
                            #  25: tango._tango.CmdArgType.DevVarLong64Array,
                            #  26: tango._tango.CmdArgType.DevVarULong64Array,
                            #  31: tango._tango.CmdArgType.DevVarStateArray}
                            elif(attr_info.data_format == AttrDataFormat.SPECTRUM):
                                res = self.add_to_metric_spectrum(dev, attr_info, attribute_metrics)
                                if(res <= 0):
                                    not_managed_attribute_count += 1
                                    #print("*******NOT MANAGED: "+attr_info.name)
                                else:
                                    spectrum_count += 1
                                    read_count += 1
                                
                            elif(attr_info.data_format == AttrDataFormat.IMAGE):
                                # res = self.add_to_metric_image(dev, attr_info, attribute_metrics)
                                # if(res <= 0):
                                not_managed_attribute_count += 1
                                #print("*******NOT MANAGED: "+attr_info.name)
                                image_count += 1
                                # read_count += 1
                            else:
                                # AttrDataFormat.FMT_UNKNOWN
                                not_managed_attribute_count += 1
                                #print("*******NOT MANAGED: "+attr_info.name)
                        except Exception as e1: 
                            #print ("Could not connect to the '"+ class_list[j] + "." + attr_info.name+"' Attribute.\r\n")
                            #print(e1)
                            error_attr_count += 1
                except Exception as e2: 
                    #print ("Could not connect to the '"+class_list[j]+"' DeviceProxy.\r\n")
                    #print(e2)
                    error_count += 1
                j += 2
            i += 1
        
        yield attribute_metrics

        errors = GaugeMetricFamily("error_count", 'Total number of errors reading the devices')
        errors.add_metric([], error_count)
        yield errors

        errors_attr = GaugeMetricFamily("error_attr_count", 'Total number of errors reading the device attributes')
        errors_attr.add_metric([], error_attr_count)
        yield errors_attr

        attribute_count = GaugeMetricFamily("attribute_count", 'Total number of attributes')
        attribute_count.add_metric([], total_count)
        yield attribute_count

        attribute_read_count = GaugeMetricFamily("attribute_read_count", 'Total number of read attributes')
        attribute_read_count.add_metric([], read_count)
        yield attribute_read_count

        spectrum_attribute_count = GaugeMetricFamily("spectrum_attribute_count", 'Total number of spectrum attributes')
        spectrum_attribute_count.add_metric([], spectrum_count)
        yield spectrum_attribute_count

        image_attribute_count = GaugeMetricFamily("image_attribute_count", 'Total number of image attributes')
        image_attribute_count.add_metric([], image_count)
        yield image_attribute_count

        not_managed = GaugeMetricFamily("not_managed_attribute_count", 'Total number of not managed attributes')
        not_managed.add_metric([], not_managed_attribute_count)
        yield not_managed

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--replica_id', help='Replica ID identification')
    parser.add_argument('-r', '--replicas', help='Replica count')

    args = parser.parse_args()

    collector = CustomCollector()

    if(args.replica_id and args.replicas):
        collector.replica_id=int(args.replica_id)
        collector.replicas=int(args.replicas)


    start_http_server(8000)
    REGISTRY.register(collector)
    while True:
        time.sleep(1)
