import React from 'react';
import {connectRedux} from '../utils';
import IdentityFormSection from './identity-form-section';
import {AnimateFade} from './animator';
import EmploymentHistoryFormSectionAdmin from './employment-history-form-section';
import PolicyFormControls from './policy-form-controls';

export default connectRedux(React.createClass({
  render() {
    return (
      <div style={{marginRight: '50px', marginLeft: '50px'}}>
        <h1>Policy Application: {this.props.store.policy.id}</h1>
        <IdentityFormSection />
        <AnimateFade>
          {this.renderEmploymentHistorySectionAdmin()}
        </AnimateFade>
      </div>
    );
  },
  renderEmploymentHistorySectionAdmin() {
    if(this.props.store.account.authenticated) {
      return (
        <div>
          <div className="divider"></div>
          <EmploymentHistoryFormSectionAdmin />
        </div>
      );
    }
    return null;
  },
}));
