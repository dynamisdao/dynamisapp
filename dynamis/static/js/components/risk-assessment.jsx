import React from 'react';
import {connectRedux} from '../utils';
import _ from 'lodash';
import actions from '../actions/actions';

export default connectRedux(React.createClass({
  render() {
    return (
      <div className="container">
        <h1>Policy Info</h1>
        <div className="row">
          <div className="col s6">
            <h2>Identities</h2>
            <ul className="collection">
              {this.props.store.riskAssessment.identities.map(this.renderIdentity)}
            </ul>
          </div>
          <div className="col s6">
            <h2>Employment History</h2>
            <ul className="collection">
              {this.props.store.riskAssessment.jobs.map(this.renderJob)}
            </ul>
          </div>
        </div>
        <div className="input-field">
          <input type="text" id="risk_assessment_estimated_claim_length"/>
          <label htmlFor="risk_assessment_estimated_claim_length">Esimated Claim Length</label>
        </div>
        <div className="input-field">
          <input type="text" id="risk_assessment_estimated_days_that_claim_wont_open"/>
          <label htmlFor="risk_assessment_estimated_days_that_claim_wont_open">Estimated Days That Claim Wont Open</label>
        </div>
        <button className="btn">Submit</button>
      </div>
    );
  },
  averageScore(identity) {
    return _.sumBy(identity.reviews, 'score') / identity.reviews.length;
  },
  renderIdentity(identity, index) {
    var score = this.averageScore(identity);
    return (
      <li key={index} className="collection-item avatar">
        <img src="https://avatars3.githubusercontent.com/u/824194?v=3&s=460" className="circle" />
        <span className="title">{identity.data.type}</span>
        <p>
          {identity.data.username}
        </p>
        {this.renderExtra(index)}
        <div className="secondary-content">
          {this.renderStars(_.round(score))}
          <br />
          ({_.round(score, 1)} From 3 reviews) {this.renderExpandMore(index)}
        </div>
      </li>
    );
  },
  renderJob(job, index) {
    var monthNames = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    return (
      <li key={index} className="collection-item">
        <span className="title">{job.company} <br />
        {monthNames[job.startMonth]} {job.startYear} - {monthNames[job.endMonth]} {job.endYear}</span>
        <p>
          {job.notes}
        </p>
      </li>
    );
  },
  renderExpandMore(index) {
    var isExpanded = this.props.store.riskAssessment.expanded === index;
    return (
      <i className="cursor-pointer material-icons" onClick={() => this.expandMore(isExpanded ? null : index)}>
        {isExpanded ? 'expand_less' : 'expand_more'}
      </i>
    );
  },
  expandMore(index) {
    this.props.dispatch(actions.setOn('riskAssessment', 'expanded', index));
  },
  renderExtra(index) {
    if(this.props.store.riskAssessment.expanded === index) {
      return (
        <div className="row">
          <div className="col s6">
            <ul className="collection">
              {this.props.store.riskAssessment.identities[index].reviews.map((review, index) => {
                return <li key={index} className="collection-item">{this.renderStars(review.score)}<br /><i>{review.reason}</i></li>;
              })}
            </ul>
          </div>
        </div>
      );
    }
  },
  renderStars(n) {
    return _.range(n).map(n => <i key={n} className="material-icons">stars</i>);
  },
}));
