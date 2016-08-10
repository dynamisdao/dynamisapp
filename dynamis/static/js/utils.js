import {connect} from 'react-redux';
import _ from 'lodash';
import types from './actions/types';
import murmurhash from 'murmurhash';

export function getQueryParams() {
  var a = window.location.search.substr(1).split('&');
  if (a === '') return {};
  var b = {};
  for (var i = 0; i < a.length; ++i) {
    var p = a[i].split('=', 2);
    if (p.length == 1) {
      b[p[0]] = '';
    }
    else
    b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, ' '));
  }
  return b;
}

export function removeIndexFromArray(array, index) {
  var left = array.slice(0, index);
  var right = array.slice(index + 1);
  return left.concat(right);
}

export function connectRedux(component) {
  return connect(function(state) {
    // redux connects its state to the `store` key
    // inside smart component `props`
    return { store: state };
  })(component);
}

export function dispatchDjangoErrorMessages(dispatch, target, errors) {
  /*
   * Django returns errors as an object of error keys which map to
   * arrays of error message strings.  This loops over that outer
   * object and the inner arrays and adds error messages for each.
   */
  _.forIn(errors, function(value, key) {
    _.map(value, function(errMsg) {
      dispatch({
        type: types.ADD_NOTIFICATION,
        message: errMsg,
        target: target,
        uuid: key + ':' + murmurhash.v3(errMsg)
      });
    });
  });
}
