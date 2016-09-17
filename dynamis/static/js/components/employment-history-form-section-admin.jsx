import React from 'react';
import {connectRedux} from '../utils';
import {AnimateFade} from './animator';
import EmploymentHistoryFormAdmin from './employment-history-form-admin';

export default connectRedux(React.createClass({
  render() {
    return (
      <div>
        <h1>Employment History</h1>
        <div>
          <AnimateFade>
            {this.renderInner()}
          </AnimateFade>
        </div>
      </div>
    );
  },
  renderInner() {
    return (
      <div key="form">
        <EmploymentHistoryFormAdmin />
      </div>
    );
  },
}));
