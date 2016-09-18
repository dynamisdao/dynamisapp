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
                    <h1>Identity: {this.props.store.policy.user.email}</h1>
                    <AnimateFade>
                        <h3>{this.props.store.policy.user.email}</h3>
                    </AnimateFade>
                </div>
                <AnimateFade>
                    Status: {this.renderPolicyStatusAdmin()}
                </AnimateFade>
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
        if (this.props.store.policy.is_final) {
            return (
                <span class="badge green">Under Review</span>
            );
        }
        else {
            return <span class="badge green">Incomplete</span>
        }
    },
}));
