import React from 'react';
import {connectRedux} from '../utils';
import Notification from './notification';
import {AnimateFade} from './animator';
import _ from 'lodash';

export default connectRedux(React.createClass({
  render() {
    var notifications = _.filter(this.props.store.notifications.notifications, {target: this.props.sectionId});
    return <AnimateFade>{notifications.map(this.renderNotification)}</AnimateFade>;
  },
  renderNotification(notification, index) {
    return (
      <Notification
        key={notification.uuid}
        notificationId={notification.uuid}
        sectionId={this.props.sectionId}
        level={notification.level}
        message={notification.message}
        dismissable={notification.dismissable} />
    );
  },
}));
