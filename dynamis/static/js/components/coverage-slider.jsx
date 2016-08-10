import React from 'react';
import {connectRedux} from '../utils';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import actions from '../actions/actions';
import _ from 'lodash';

export default connectRedux(React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState() {
    return {sliderValue: '250'};
  },
  render() {
    var premium = this.props.store.policy.premium;
    return (
      <div>
        <h1>Coverage Amount</h1>
        Hello user, this section is only an estimate of what you might get.
        <div className="container">
          <div className="range-field">
            ${this.fancyAlgorithm(premium)} coverage/week
            <input type="range" min="1" max="500" value={premium} onChange={this.onPremiumChange}/>
            ${premium}/mo premium
          </div>
        </div>
      </div>
    );
  },
  componentWillMount: function() {
    this.debounceSavePolicy = _.debounce(() => this.props.dispatch(actions.savePolicy()), 500);
  },
  onPremiumChange(e) {
    this.props.dispatch(actions.setOn('policy', 'premium', e.target.value));
    this.debounceSavePolicy();
  },
  fancyAlgorithm(n) {
    return parseInt(n) * 2;
  },
}));
