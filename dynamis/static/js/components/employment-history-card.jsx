import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';
import FileIcon from './file-icon';
import _ from 'lodash';
import {STATES} from '../constants';
import NotificationPanel from './notification-panel';

export default connectRedux(React.createClass({
  render() {
    return (
      <div className="card">
        <NotificationPanel sectionId={'job_' + this.props.jobId} />
        <div className="row">
          {this.renderMonthSelect('startMonth', 'Start')}
          {this.renderYearSelect('startYear', 'Start')}
          {this.renderMonthSelect('endMonth', 'End', true)}
          {this.renderYearSelect('endYear', 'End', true)}

          <input type="checkbox" checked={this.getData('currentJob')} onChange={this.linkCheckbox('currentJob')} id={'employment_current_checkbox_' + this.props.jobId} />
          <label htmlFor={'employment_current_checkbox_' + this.props.jobId}>I currently work here</label>

        </div>
        <div className="row">
          <p>An employment history record <em>should</em> contain as many of the following pieces of information as possible</p>
          <ul>
            <li><strong>Job Title</strong></li>
            <li><strong>Why you left</strong></li>
            <li><strong>How to verify</strong> (Who can verify your employment, how can someone reach them, how can someone verify that they are who you say they are).</li>
          </ul>
        </div>
        <div className="row">
          <div className="input-field col s3">
            <label htmlFor={'employment_company_' + this.props.jobId}>Company Name</label>
            <input type="text" value={this.getData('company')} onChange={this.linkStore('company')} id={'employment_company_' + this.props.jobId} />
          </div>
        </div>
        <div className="row">
          <div className="input-field">
            <label htmlFor={'employment_notes_' + this.props.jobId}>Job Info</label>
            <textarea value={this.getData('notes')} onChange={this.linkStore('notes')} className="materialize-textarea" id={'employment_notes_' + this.props.jobId} />
          </div>
        </div>
        <div className="row">
          <div className="input-field">
            <input className="hidden-file-input" id={'employment_files_' + this.props.jobId} type="file" multiple onChange={this.readFileIntoStore} />
            <label className="btn" htmlFor={'employment_files_' + this.props.jobId}>Select Files</label><br /><br />
          </div>
          <div className="input-field">
            {this.getData('files', []).map((file, index) => {
              return <FileIcon key={index} jobId={this.props.jobId} fileId={index} file={file} />;
            })}
          </div>
        </div>
        <div className="row">
          <div>
            <button className="btn" onClick={this.persistChanges}>Save</button>
            <button className="btn" onClick={this.discardChanges}>Cancel</button>
            {this.renderRemoveButton()}
          </div>
        </div>
      </div>
    );
  },
  componentDidMount() {
    Materialize.updateTextFields();
  },
  renderYearSelect(fieldName, info, disable) {
    var thisYear = (new Date()).getFullYear();
    return (
      <div className="input-field col s2">
        <select disabled={disable && this.getData('currentJob')} className="browser-default" defaultValue="year" value={this.getData(fieldName)} onChange={this.linkStore(fieldName)}>
          <option value="year" disabled>{info} Year</option>
          <option value={thisYear    }>{thisYear    }</option>
          <option value={thisYear - 1}>{thisYear - 1}</option>
          <option value={thisYear - 2}>{thisYear - 2}</option>
          <option value={thisYear - 3}>{thisYear - 3}</option>
          <option value={thisYear - 4}>{thisYear - 4}</option>
          <option value={thisYear - 5}>{thisYear - 5}</option>
          <option value={thisYear - 6}>{thisYear - 6}</option>
          <option value={thisYear - 7}>{thisYear - 7}</option>
          <option value={thisYear - 8}>{thisYear - 8}</option>
        </select>
      </div>
    );
  },
  renderMonthSelect(fieldName, info, disable) {
    return (
      <div className="input-field col s2">
        <select disabled={disable && this.getData('currentJob')} className="browser-default" defaultValue="month" value={this.getData(fieldName)} onChange={this.linkStore(fieldName)}>
          <option value="month" disabled>{info} Month</option>
          {this.renderMonthOptions()}
        </select>
      </div>
    );
  },
  renderMonthOptions() {
    var monthNames = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    var options = [];
    for (var i = 0; i < 12; i++) {
      options.push(<option key={i} value={i}>{monthNames[i]}</option>);
    }
    return options;
  },
  readFileIntoStore(event) {
    var props = this.props;
    _.map(event.target.files, function(file) {
      var reader = new FileReader();
      reader.onload = function(event) {
        props.dispatch(actions.addFileToEmploymentHistory(props.jobId, file.name, file.type, event.target.result));
      };
      reader.readAsDataURL(file);
    });
  },
  linkStore(fieldName) {
    var props = this.props;
    return function(event) {
      props.dispatch(actions.updateEmploymentHistoryJob(props.jobId, fieldName, event.target.value));
      props.dispatch(actions.validateEmploymentHistoryJob(props.jobId));
    };
  },
  linkCheckbox(fieldName) {
    var props = this.props;
    return function(event) {
      props.dispatch(actions.updateEmploymentHistoryJob(props.jobId, fieldName, event.target.checked));
      props.dispatch(actions.validateEmploymentHistoryJob(props.jobId));
    };
  },
  getData(fieldName, defaultValue) {
    return _.get(this, 'props.store.employmentHistory.jobs['+this.props.jobId+'].current.'+fieldName, defaultValue);
  },
  persistChanges() {
    this.props.dispatch(actions.toggleEmploymentHistoryEdit(this.props.jobId));
    this.props.dispatch(actions.savePolicy());
  },
  discardChanges() {
    this.props.dispatch(actions.discardEmploymentHistoryChanges(this.props.jobId));
  },
  removeJob() {
    this.props.dispatch(actions.removeEmploymentHistoryJob(this.props.jobId));
    this.props.dispatch(actions.savePolicy());
  },
  renderRemoveButton() {
    if(this.getData('state') != STATES.NEW) {
      return <button className="btn" onClick={this.removeJob}>Remove</button>;
    }
  },
}));
