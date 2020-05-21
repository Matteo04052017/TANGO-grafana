import { PanelPlugin } from '@grafana/data';
import { TableOptions } from './types';
import { AttributePanel } from './AttributePanel';

export const plugin = new PanelPlugin<TableOptions>(AttributePanel).setPanelOptions(builder => {
  return builder
    .addBooleanSwitch({
      path: 'pagination',
      name: 'Show pagination',
      defaultValue: false,
    })
    .addBooleanSwitch({
      path: 'header',
      name: 'Show header',
      defaultValue: false,
    })
    .addBooleanSwitch({
      path: 'dense',
      name: 'Dense',
      defaultValue: false,
    })
    .addBooleanSwitch({
      path: 'tablehead',
      name: 'Show table head',
      defaultValue: false,
    });
});
