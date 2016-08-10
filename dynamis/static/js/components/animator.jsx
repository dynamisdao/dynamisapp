import React from 'react';
import Animator from 'react-addons-css-transition-group';

export function AnimateFade(props) {
  return (
    <Animator transitionName="animation-fade" transitionEnterTimeout={500} transitionLeaveTimeout={300} >
      {props.children}
    </Animator>
  );
}
