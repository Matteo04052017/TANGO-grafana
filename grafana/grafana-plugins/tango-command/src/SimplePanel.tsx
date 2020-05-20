import React, { useState } from 'react';
import { PanelProps } from '@grafana/data';
import { SimpleOptions } from 'types';

interface Props extends PanelProps<SimpleOptions> {}

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [dataRes, setDataRes] = useState('');

  let handleClick = () => {
    fetch(options.url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'no-cors', // no-cors, *cors, same-origin
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
    }).then(
      result => {
        setIsLoaded(true);
        console.log(result);
        setDataRes(result.toString());
      },
      // Note: it's important to handle errors here
      // instead of a catch() block so that we don't swallow
      // exceptions from actual bugs in components.
      error => {
        setIsLoaded(true);
        setError(error);
      }
    );
  };

  if (error) {
    return <div>Error: {error}</div>;
  } else if (!isLoaded) {
    return <button onClick={handleClick}>Call command!</button>;
  } else {
    return <div>{dataRes}</div>;
  }
};
