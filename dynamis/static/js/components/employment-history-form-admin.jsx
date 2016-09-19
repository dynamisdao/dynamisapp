import React from 'react';
import {connectRedux} from '../utils';
import EmploymentHistoryProgress from './employment-history-progress';
import EmploymentHistoryCompletedAdmin from './employment-history-completed-admin';
import {STATES} from '../constants';
import _ from 'lodash';

export default connectRedux(React.createClass({
  render() {
    return (
      <div className="section">
        <EmploymentHistoryProgress jobs={this.props.store.employmentHistory.jobs} />
        {this.props.store.employmentHistory.jobs.map((cardData, index) => {
          if (cardData.current.state === STATES.READ_ONLY) {
            return <EmploymentHistoryCompletedAdmin key={index} jobId={index} jobData={cardData.current} />;
          }
        })}
      </div>
    );
  },
}));
