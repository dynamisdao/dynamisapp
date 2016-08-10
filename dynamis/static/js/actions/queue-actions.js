import urls from '../urls';
import types from './types';
import {dispatchDjangoErrorMessages} from '../utils';
import {setOn} from './gourmet-redux';

export function loadP2PQueue() {
  return function(dispatch, getState) {
    dispatch({
      type: types.CLEAR_NOTIFICATIONS,
      target: 'review',
    });
    $.get(urls['application-item-list']).done(data => {
      dispatch({type: types.LOAD_P2P_QUEUE, tasks: data.results});
    }).error(response => {
      dispatchDjangoErrorMessages(dispatch, 'review', response.responseJSON);
    });
    dispatch(getReviewHistory());
  };
}

export function submitReview(id, signature) {
  return function(dispatch, getState) {
    dispatch({
      type: types.CLEAR_NOTIFICATIONS,
      target: 'review',
    });
    $.post({
      url: urls['application-item-list'] + id + '/submit-peer-review/',
      data: JSON.stringify({ signed_message: signature }),
      contentType: 'application/json',
    }).done(function(data) {
      dispatch(loadP2PQueue());
    }).error(function(response) {
      dispatchDjangoErrorMessages(dispatch, 'review', response.responseJSON);
    });
  };
}

export function getReviewHistory() {
  return function(dispatch, getState) {
    $.get(urls['peer-review-history']).done(function(data) {
      var history = data.results.map(function(item) {
        var app = JSON.parse(item.data).policy_application;
        return { ...app, type: item.application_item.type};
      });
      dispatch(setOn('queue', 'history', history));
    });
  };
}
