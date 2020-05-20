import { PanelPlugin } from '@grafana/data';
import { SimpleOptions } from './types';
import { SimplePanel } from './SimplePanel';

export const plugin = new PanelPlugin<SimpleOptions>(SimplePanel).setPanelOptions(builder => {
  return builder
    .addTextInput({
      path: 'url',
      name: 'Tango GQL web url',
      description: 'Tango GQL web url',
      defaultValue: 'https://integration.engageska-portugal.pt/testdb/graphiql/',
    })
    .addTextInput({
      path: 'username',
      name: 'Username',
      description: 'Username',
      defaultValue: 'user1',
    })
    .addTextInput({
      path: 'password',
      name: 'Password',
      description: 'Password',
      defaultValue: 'abc123',
    })
    .addTextInput({
      path: 'mutation',
      name: 'TangoGQL mutation',
      description: 'TangoGQL mutation',
      defaultValue: '',
    });
});
