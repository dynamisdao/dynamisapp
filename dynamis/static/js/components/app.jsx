import React from 'react';
import {connectRedux} from '../utils';

export default connectRedux(React.createClass({
  render() {
    return (
      <div>
        <h1>
          Hello Josh
        </h1>
      </div>
    );
  }
}));
