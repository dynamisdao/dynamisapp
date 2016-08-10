import React from 'react';
import {connectRedux} from '../utils';
import {AnimateFade} from './animator';
import EmploymentHistoryForm from './employment-history-form';

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
        <EmploymentHistoryForm />
      </div>
    );
  },
}));
