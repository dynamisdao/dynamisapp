import React from 'react';
import {connectRedux} from '../utils';
import EmploymentHistoryCard from './employment-history-card';
import EmploymentHistoryProgress from './employment-history-progress';
import EmploymentHistoryCompleted from './employment-history-completed';
import actions from '../actions/actions';
import {STATES} from '../constants';
import _ from 'lodash';

export default connectRedux(React.createClass({
  render() {
    return (
      <div className="section">
        <EmploymentHistoryProgress jobs={this.props.store.employmentHistory.jobs} />
        {this.props.store.employmentHistory.jobs.map((cardData, index) => {
          if (cardData.current.state === STATES.READ_ONLY) {
            return <EmploymentHistoryCompleted key={index} jobId={index} jobData={cardData.current} />;
          } else {
            return <EmploymentHistoryCard key={index} jobId={index} />;
          }
        })}
        {this.renderControls()}
      </div>
    );
  },
  addEmploymentHistoryCard() {
    this.props.dispatch(actions.addEmploymentHistoryJob());
  },
  renderDoneButton() {
    if(_.some(this.props.store.employmentHistory.jobs, 'saved')) {
      return <button className="btn" onClick={this.markDone}>Done Adding Jobs</button>;
    }
  },
  markDone() {
    this.props.dispatch(actions.markEmploymentHistoryDone());
  },
  markNotDone() {
    this.props.dispatch(actions.markEmploymentHistoryNotDone());
  },
  renderControls() {
    if(this.props.store.employmentHistory.done) {
      return <button className="btn" onClick={this.markNotDone}>Not Done</button>;
    } else {
      return (
        <div>
          <button className="btn" onClick={this.addEmploymentHistoryCard}>
            Add Job
          </button>
          {this.renderDoneButton()}
        </div>
      );
    }
  },
}));
