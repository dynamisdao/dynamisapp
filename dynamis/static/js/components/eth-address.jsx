import React from 'react';
import _ from 'lodash';
import EthAddressIcon from './eth-address-icon';
import EthAddressHex from './eth-address-hex';

export default React.createClass({
  getDefaultProps() {
    return {
      extraClasses: [],
    };
  },
  render() {
    var classes = _.flatten(['eth-address'], this.props.extraClasses);
    return (
      <span className={_.join(classes, ' ')}>
        <EthAddressIcon {...this.props} /><EthAddressHex {...this.props} />
      </span>
    );
  }
});
