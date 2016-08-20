import React from 'react';
import {connectRedux} from '../utils';

export default connectRedux(React.createClass({
  render() {
    return (
      <div>
        <h1>
          Hello! 
        </h1>
      </div>
    );
  }
}));
