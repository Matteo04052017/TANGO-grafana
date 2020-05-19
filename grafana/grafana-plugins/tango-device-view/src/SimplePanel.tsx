import React from 'react';
import { PanelProps } from '@grafana/data';
import { SimpleOptions } from 'types';
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
    name: 'Name',
    selector: 'name',
    sortable: true,
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

interface Props extends PanelProps<SimpleOptions> {}

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
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

    //console.log('adding ' + device_attributes[i]?.labels?.name + ' value=' + this_value + ']');
    attributes.push({
      name: device_attributes[i]?.labels?.name,
      value: this_value,
    });
  }

  let last_name = 'init';
  let last_value = '[';
  for (let i = 0; i < device_attributes_spectrum.length; i++) {
    let this_name = device_attributes_spectrum[i]?.labels?.name;
    // console.log('processing ' + this_name);
    if (!this_name) {
      continue;
    }
    if (attributes.find(attr => attr.name === this_name)) {
      continue;
    }

    let j = device_attributes_spectrum[i]?.values.length;
    if (!j) {
      j = 1;
    }
    let this_value = device_attributes_spectrum[i]?.values?.get(j - 1);
    if (
      device_attributes_spectrum[i]?.labels?.type === 'string' ||
      device_attributes_spectrum[i]?.labels?.type === 'state'
    ) {
      this_value = device_attributes_spectrum[i]?.labels?.str_value;
    }

    // console.log('this_name=' + this_name);
    // console.log('last_name=' + last_name);

    if (last_name === 'init') {
      last_name = this_name;
    }
    if (this_name === last_name) {
      if (last_value === '[') {
        last_value = '[' + this_value;
      } else {
        last_value = last_value + ',' + this_value;
      }
    }
    if (this_name !== last_name) {
      attributes.push({
        name: last_name,
        value: last_value + ']',
      });
      last_name = this_name;
      last_value = '[' + this_value;
    }
  }

  // console.log('attributes length ' + attributes.length);

  return (
    <DataTable
      title="Attributes list"
      columns={columns}
      data={attributes}
      theme="solarized"
      customStyles={customStyles}
    />
  );
};
