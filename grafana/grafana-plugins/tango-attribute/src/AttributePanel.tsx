import React from 'react';
import { PanelProps } from '@grafana/data';
import { TableOptions } from 'types';
import DataTable, { createTheme } from 'react-data-table-component';

// https://github.com/jbetancur/react-data-table-component/blob/master/src/DataTable/themes.js
createTheme('solarized', {
  text: {
    primary: '#268bd2',
    secondary: '#2aa198',
  },
  background: {
    default: '#002b36',
  },
  context: {
    background: '#cb4b16',
    text: '#FFFFFF',
  },
  divider: {
    default: '#073642',
  },
  sortFocus: {
    default: 'white',
  },
});

// https://github.com/jbetancur/react-data-table-component/blob/master/src/DataTable/styles.js
const customStyles = {
  headCells: {
    style: {
      fontSize: '18px',
      fontWeight: 800,
    },
  },
};

// https://github.com/jbetancur/react-data-table-component#columns
const columns = [
  {
    name: 'Device',
    selector: 'device',
    sortable: true,
    width: '230px',
  },
  {
    name: 'Name',
    selector: 'name',
    sortable: true,
    width: '230px',
  },
  {
    name: 'Value',
    selector: 'value',
    sortable: true,
    wrap: true,
    conditionalCellStyles: [
      {
        when: (row: any) => row.value === 'ON',
        style: {
          backgroundColor: 'rgba(63, 195, 128, 0.9)',
          color: 'white',
          '&:hover': {
            cursor: 'pointer',
          },
        },
      },
      {
        when: (row: any) => row.value === 'OFF',
        style: {
          backgroundColor: 'rgba(242, 38, 19, 0.9)',
          color: 'white',
          '&:hover': {
            cursor: 'not-allowed',
          },
        },
      },
    ],
  },
];

interface Props extends PanelProps<TableOptions> {}

export const AttributePanel: React.FC<Props> = ({ options, data, width, height }) => {
  const device_attributes = data.series.map(series =>
    series.fields.find(field => field.type === 'number' && field.labels?.dim_x === '1' && field.labels?.dim_y === '0')
  );

  const device_attributes_spectrum = data.series.map(series =>
    series.fields.find(field => field.type === 'number' && field.labels?.dim_x !== '1' && field.labels?.dim_y === '0')
  );

  // const device_attributes_image = data.series.map(series => series.fields.find(field => field.type === 'number' && field.labels?.dim_x !== "1" && field.labels?.dim_y !== "0"));
  //console.log(device_attributes_spectrum);
  const attributes = [];

  for (let i = 0; i < device_attributes.length; i++) {
    if (!device_attributes[i]?.labels?.name) {
      continue;
    }

    let j = device_attributes[i]?.values.length;
    if (!j) {
      j = 1;
    }
    let this_value = device_attributes[i]?.values?.get(j - 1);
    if (device_attributes[i]?.labels?.type === 'string' || device_attributes[i]?.labels?.type === 'state') {
      this_value = device_attributes[i]?.labels?.str_value;
    }

    attributes.push({
      device: device_attributes[i]?.labels?.device,
      name: device_attributes[i]?.labels?.name,
      value: this_value,
    });
  }

  let device_attributes_spectrum_sorted = device_attributes_spectrum.sort((a, b) => {
    if (a?.labels?.x && b?.labels?.x) {
      return parseInt(a?.labels?.x, 10) - parseInt(b?.labels?.x, 10);
    } else {
      return 0;
    }
  });

  for (let i = 0; i < device_attributes_spectrum_sorted.length; i++) {
    let this_device = device_attributes_spectrum_sorted[i]?.labels?.device;
    let this_name = device_attributes_spectrum_sorted[i]?.labels?.name;

    console.log('processing ' + this_name);
    if (!this_name) {
      continue;
    }

    let j = device_attributes_spectrum_sorted[i]?.values.length;
    if (!j) {
      continue;
    }
    let this_value = device_attributes_spectrum_sorted[i]?.values?.get(j - 1);
    if (
      device_attributes_spectrum_sorted[i]?.labels?.type === 'string' ||
      device_attributes_spectrum_sorted[i]?.labels?.type === 'state'
    ) {
      this_value = device_attributes_spectrum_sorted[i]?.labels?.str_value;
    }

    let already_stored = attributes.find(attr => attr.name === this_name && attr.device === this_device);
    if (already_stored) {
      already_stored.value = already_stored.value + ';\t\t' + this_value;
    } else {
      attributes.push({
        device: this_device,
        name: this_name,
        value: this_value,
      });
    }
  }

  return (
    <DataTable
      title="Attributes list"
      columns={columns}
      data={attributes}
      theme="solarized"
      customStyles={customStyles}
      pagination={options.pagination}
      dense={options.dense}
      noTableHead={options.tablehead}
      noHeader={options.header}
    />
  );
};
