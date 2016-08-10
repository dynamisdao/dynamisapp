import _ from 'lodash';

function Reducer(name, initialState) {
  this.name = name;
  this.subscriptions = {};
  this.initialState = initialState;
}

Reducer.prototype.subscribe = function(type, fun) {
  if(!type) {
    // eslint-disable-next-line no-console
    console.error('type is blank');
  }
  if(this.subscriptions[type]) {
    // eslint-disable-next-line no-console
    console.error('you have already subscribed to', type);
  }
  if(!fun) {
    // eslint-disable-next-line no-console
    console.error('no function passed in');
  }
  this.subscriptions[type] = fun;
};

Reducer.prototype.build = function () {
  var subscriptions = this.subscriptions;
  var initialState = this.initialState;
  var name = this.name;

  return function(state = initialState, action) {
    if(subscriptions[action.type]) {
      return subscriptions[action.type](_.cloneDeep(state), action);
    }
    if(_.startsWith(action.type, `SET.${name}.`)) {
      // eslint-disable-next-line no-console
      console.error(`Action with type '${action.type}' was called but the ${name} reducer is not subscribed to this action`);
    }
    return state;
  };
};

Reducer.prototype.addSetter = function (key) {
  this.subscribe(`SET.${this.name}.${key}`, function(state, action) {
    var newValue = {};
    newValue[key] = action[key];
    return {
      ...state,
      ...newValue
    };
  });
};

export default Reducer;
