import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';

export default connectRedux(React.createClass({
  render() {
    return (
      <div className={this.getColor()} style={{padding: '10px'}}>
        {this.props.message}
        {this.renderDismissButton()}
      </div>
    );
  },
  dismiss() {
    this.props.dispatch(actions.dismissNotification(this.props.notificationId, this.props.sectionId));
  },
  getColor() {
    return {
      ERROR: 'red lighten-3',
      SUCCESS: 'green',
      WARNING: 'yellow',
      INFO: 'light-blue',
    }[this.props.level];
  },
  renderDismissButton() {
    if(this.props.dismissable) {
      return <i style={{cursor: 'pointer'}} className="material-icons" onClick={this.dismiss}>close</i>;
    }
  },
}));
