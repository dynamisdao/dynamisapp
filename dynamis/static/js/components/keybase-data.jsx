import React from 'react';

export default function KeybaseData(props) {
  return (
    <div className="chip">
      <img src={props.data.picture} />
      {props.data.username}
    </div>
  );
}
