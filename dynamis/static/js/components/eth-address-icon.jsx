import React from 'react';
import _ from 'lodash';
import {createIcon} from '../blockies';

export default React.createClass({
  getDefaultProps() {
    return {
      address: '0x0000000000000000000000000000000000000000',
      size: 'large',
      extraClasses: [],
    };
  },
  getDataURL() {
    var address = this.props.address;
    if(!_.startsWith(address, '0x')) {
      address = '0x' + address;
    }
    return createIcon({
      seed: address,
      size: 8,
      scale: 16
    }).toDataURL();
  },
  render() {
    var defaultClasses = ['eth-address-icon', 'eth-address-icon-' + this.props.size];
    var classes = _.flatten(defaultClasses, this.props.extraClasses);

    return <img className={_.join(classes, ' ')} src={this.getDataURL()} />;
  }
});
