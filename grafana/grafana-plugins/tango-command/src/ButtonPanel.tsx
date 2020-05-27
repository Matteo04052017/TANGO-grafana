import React, { useState } from 'react';
import { PanelProps } from '@grafana/data';
import { ButtonOptions } from 'types';
import './button.css';

interface Props extends PanelProps<ButtonOptions> {}

export const ButtonPanel: React.FC<Props> = ({ options, data, width, height }) => {
  const [error, setError] = useState('');

  const handleClick = async () => {
    const result = await fetch(options.url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json',
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify({
        mutation: options.mutation,
        username: options.username,
        password: options.password,
      }), // body data type must match "Content-Type" header
    });
    console.log(result);
    const json = await result.json();
    console.log(json);
    console.log(result.body);
    console.log(result.bodyUsed);
    console.log(typeof json);
    if (!result.ok) {
      setError(result.statusText);
      return;
    }
    if (json['data']['executeCommand']['ok']) {
      alert('Command executed successfully. ');
    } else {
      setError(json['data']['executeCommand']['message']);
      alert('Command failed!');
    }
  };

  return (
    <div>
      {error && <div>{error}</div>}
      <button className="mybutton" onClick={handleClick}>
        {options.button_text}
      </button>
    </div>
  );
};
