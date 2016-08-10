import React from 'react';
import {connectRedux} from '../utils';
import IdentityFormSection from './identity-form-section';
import {AnimateFade} from './animator';
import AccountCreationFormSection from './account-creation-form-section';
import EmploymentHistoryFormSection from './employment-history-form-section';
import PolicyFormControls from './policy-form-controls';
import CoverageSlider from './coverage-slider';

export default connectRedux(React.createClass({
  render() {
    return (
      <div style={{marginRight: '50px', marginLeft: '50px'}}>
        <h1>Policy Application: {this.props.store.policy.id}</h1>
        <IdentityFormSection />
        <AnimateFade>
          {this.renderAccountCreationSection()}
        </AnimateFade>
        <AnimateFade>
          {this.renderEmploymentHistorySection()}
        </AnimateFade>
        <AnimateFade>
          {this.renderSubmissionControls()}
        </AnimateFade>
      </div>
    );
  },
  renderAccountCreationSection() {
    if(this.props.store.keybase.username) {
      return (
        <div>
          <div className="divider"></div>
          <AccountCreationFormSection />
        </div>
      );
    }
    return null;
  },
  renderEmploymentHistorySection() {
    if(this.props.store.account.authenticated) {
      return (
        <div>
          <div className="divider"></div>
          <EmploymentHistoryFormSection />
        </div>
      );
    }
    return null;
  },
  renderSubmissionControls() {
    if(this.props.store.employmentHistory.done) {
      return (
        <div>
          <div className="divider"></div>
          <CoverageSlider />
          <div className="divider"></div>
          <PolicyFormControls />
        </div>
      );
    }
  },
}));
