import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';

export default connectRedux(React.createClass({
  render() {
    var monthNames = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    return (
      <div className="card">
        <ul className="collection">
          <li className="collection-item">From: {monthNames[this.props.jobData.startMonth]} {this.props.jobData.startYear}</li>
          <li className="collection-item">To: {monthNames[this.props.jobData.endMonth]} {this.props.jobData.endYear}</li>
          <li className="collection-item">Notes: {this.props.jobData.notes}</li>
          <li className="collection-item">Company: {this.props.jobData.company}</li>
          {this.props.jobData.files.map((file, index) => {
            return (
              <li key={index} className="collection-item">File: {file.name} ({file.mimetype}) <a target="_blank" href={'http://gateway.ipfs.io/ipfs/' + file.ipfsHash}>download</a></li>
            );
          })}
        </ul>
        {this.renderControls()}
      </div>
    );
  },
  editJob() {
    this.props.dispatch(actions.toggleEmploymentHistoryEdit(this.props.jobId));
  },
  removeJob() {
    this.props.dispatch(actions.removeEmploymentHistoryJob(this.props.jobId));
    this.props.dispatch(actions.savePolicy());
  },
  renderControls() {
    if(!this.props.store.employmentHistory.done) {
      return (
        <div className="card-action right-align">
          <button className="btn" onClick={this.editJob}>Edit</button>
          <button className="btn red" onClick={this.removeJob}>Remove</button>
        </div>
      );
    }
  },
}));
