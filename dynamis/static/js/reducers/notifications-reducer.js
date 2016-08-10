import types from '../actions/types';
import _ from 'lodash';
import uuid from 'uuid';

var initialState = {
  notifications: []
};

export default function(state = initialState, action = {}) {
  var notifications = _.cloneDeep(state.notifications);
  if(action.type == types.DISMISS_NOTIFICATION) {
    return {
      ...state,
      notifications: _.reject(notifications, {uuid: action.notificationId}),
    };
  } else if(action.type == types.ADD_NOTIFICATION) {
    notifications = _.reject(notifications, {uuid: action.uuid});
    return {
      ...state,
      notifications: notifications.concat({
        target: action.target,
        level: action.level || 'ERROR',
        message: action.message,
        dismissable: action.dismissable || false,
        uuid: action.uuid || uuid.v4(),
      }),
    };
  } else if(action.type == types.CLEAR_NOTIFICATIONS) {
    return {
      ...state,
      notifications: _.reject(notifications, {target: action.target}),
    };
  } else if(action.type == types.CLEAR_AND_ADD_NOTIFICATION) {
    return {
      ...state,
      notifications: _.reject(notifications, {target: action.target}).concat({
        target: action.target,
        level: action.level || 'ERROR',
        message: action.message,
        dismissable: action.dismissable || false,
        uuid: action.uuid || uuid.v4(),
      }),
    };
  }
  return state;
}
