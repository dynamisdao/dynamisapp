import React from 'react';
import {connectRedux} from '../utils';
import {AnimateFade} from './animator';
import EmploymentHistoryFormSectionAdmin from './employment-history-form-section-admin';

export default connectRedux(React.createClass({
    render() {
        return (
            <div style={{marginRight: '50px', marginLeft: '50px'}}>
                <h1>Policy Application: {this.props.store.policy.id}</h1>
                <div>
                    <h3>Identity:</h3>
                    <AnimateFade>
                        <h3>{this.props.store.policy.keybaseUsername}</h3>
                    </AnimateFade>
                </div>
                <div>
                    <h3>Policy Status:</h3>
                    <AnimateFade>
                        {this.renderPolicyStatusAdmin()}
                    </AnimateFade>
                </div>
                <AnimateFade>
                    {this.renderEmploymentHistorySectionAdmin()}
                </AnimateFade>
            </div>
        );
    },
    renderEmploymentHistorySectionAdmin() {
        if (this.props.store.account.authenticated) {
            return (
                <div>
                    <div className="divider"></div>
                    <EmploymentHistoryFormSectionAdmin />
                </div>
            );
        }
        return null;
    },

    renderPolicyStatusAdmin() {
        if (this.props.store.policy.done) {
            return (
                <span class="badge green">Incomplete</span>
            );
        }
        else {
            return <span class="badge green">Under Review</span>
        }
    },
}));
