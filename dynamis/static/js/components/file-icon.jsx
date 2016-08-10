import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';

export default connectRedux(React.createClass({
  render() {
    return (

      <div className="chip">
        <i className="material-icons">attachment</i>
        {this.props.file.name} ({this.props.file.mimetype})
        <i className="material-icons" onClick={this.removeFile}>close</i>
      </div>
    );
  },
  removeFile(event) {
    this.props.dispatch(actions.removeFileFromEmploymentHistory(this.props.jobId, this.props.fileId));
  }
}));
