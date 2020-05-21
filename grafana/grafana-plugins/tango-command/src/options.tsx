import { PanelOptionsEditorBuilder } from '@grafana/data';
import { ButtonOptions } from './types';

export const optionsBuilder = (builder: PanelOptionsEditorBuilder<ButtonOptions>) => {
  // Global options
  builder
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
    })
    .addTextInput({
      path: 'button_text',
      name: 'Button Text',
      description: 'Button Text',
      defaultValue: 'Call command!',
    });
  // .addCustomEditor({
  //   id: 'mutation',
  //   path: 'mutation',
  //   name: 'TangoGQL mutation',
  //   description: 'TangoGQL mutation',
  //   editor: props => {
  //     return (
  //       <div>
  //         <Input type="text" value={props.value} aria-multiline="true" />
  //       </div>
  //     );
  //   },
  //   defaultValue: '',
  // });
};
