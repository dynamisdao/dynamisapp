import React from 'react';
import {connectRedux} from '../utils';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import EthAddress from './eth-address';
import actions from '../actions/actions';
import download from 'downloadjs';

export default connectRedux(React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState() { return {}; },
  componentDidMount() {
    var dispatch = this.props.dispatch;
    setInterval(function() {
      dispatch(actions.readFromWeb3());
    }, 20000); // 20 seconds
  },
  render() {
    var wallet = this.props.store.wallet;
    return (
      <div className="container">
        {this.renderAddress(wallet)}
        <label htmlFor="eth_password">Password</label>
        <input type="text" id="eth_password" valueLink={this.linkState('password')} />
        <div className="card">
          <div className="card-action">
            <label htmlFor="eth_to_address">To Address</label>
            <input readOnly="True" type="text" id="eth_to_address" value={document.getElementById('address_to_send_eth').textContent} />
            <label htmlFor="eth_to_address">Amount</label>
            <input readOnly="True" type="text" id="amount" value={parseInt(document.getElementsByClassName('cost_wei')[1].textContent)} />
            <button className="btn" onClick={this.makeTransaction}>Pay Smart deposit</button>
          </div>
        </div>
      </div>
    );
  },
  readFileIntoStore(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    var dispatch = this.props.dispatch;
    reader.onload = function(event) {
      dispatch(actions.readWallet(event.target.result));
    };
    reader.readAsText(file);
  },
  generateWallet() {
    this.props.dispatch(actions.createWallet(this.state.password));
  },
  makeTransaction() {
      var xhr = new XMLHttpRequest();
      var json = JSON.stringify({
          amount_in_wei: parseInt(document.getElementsByClassName('cost_wei')[1].textContent),
          from_address: document.getElementsByClassName('eth-address-hex')[0].textContent,
      });
      var policy_id = parseInt(document.URL.split('/')[4]);
      var url_array = ["/api/v1/policies", policy_id, "smart_deposit/send"];
      var url = url_array.join('/');
      xhr.open("POST", url, true);
      xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
      xhr.send(json);

    this.setState({ toAddress: '', amount: '' });
    this.props.dispatch(actions.makeTransaction(document.getElementById('address_to_send_eth').textContent,
        parseInt(document.getElementsByClassName('cost_wei')[1].textContent), this.state.password));
  },
  renderAddress(wallet) {
    if(wallet.address) {
      return (
        <div>
          <EthAddress address={wallet.address} />
          <br />
          Wei: <code>{wallet.value || (wallet.connected ? 'loading' : 'cannot connect')}</code>
        </div>
      );
    }
  },
  changeWeb3Url() {
    if((this.state.web3url || '').trim() === '') { return; }
    this.setState({web3url: ''});
    this.props.dispatch(actions.setWeb3Url(this.state.web3url));
  },
  downloadWallet() {
    download(this.props.store.wallet.keystore.serialize(), 'wallet.json', 'application/json');
  },
}));
