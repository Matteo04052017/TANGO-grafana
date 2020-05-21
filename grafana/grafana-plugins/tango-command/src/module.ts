import { PanelPlugin } from '@grafana/data';
import { ButtonOptions } from './types';
import { ButtonPanel } from './ButtonPanel';
import { optionsBuilder } from './options';

export const plugin = new PanelPlugin<ButtonOptions>(ButtonPanel).setNoPadding().setPanelOptions(optionsBuilder);
