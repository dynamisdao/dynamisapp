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
        Our nodes:
        <ul>
          <li>TestNet (legacy server) - http://52.36.158.26:8545/</li>
          <li>TestNet - http://52.16.72.86:8545/</li>
        </ul>
        <br />
        Current rpc node host: <code className="grey lighten-2" style={{padding: '2px'}}>{wallet.web3url}</code>
        {!wallet.connected && <span><i className="material-icons">report_problem</i>Connection Failed</span>}
        <h2>{wallet.network}</h2>
        <input type="text" id="web3url" valueLink={this.linkState('web3url')} />
        <div className="row">
          <div className="input-field col s3">
            <button className="btn" onClick={this.changeWeb3Url}>Change</button>
          </div>
        </div>
        <br />
        <br />

        {this.renderAddress(wallet)}
        <label htmlFor="eth_password">Password</label>
        <input type="text" id="eth_password" valueLink={this.linkState('password')} />
        {this.renderWalletButton()}
        <div className="card">
          <div className="card-action">
            <label htmlFor="eth_to_address">To Address</label>
            <input type="text" id="eth_to_address" valueLink={this.linkState('toAddress')} />
            <label htmlFor="eth_to_address">Amount</label>
            <input type="text" id="eth_to_address" valueLink={this.linkState('amount')} />
            <button className="btn" onClick={this.makeTransaction}>Send transaction</button>
          </div>
        </div>
        <label htmlFor="wallet_upload" className="btn">Upload your wallet</label>
        <input type="file" onChange={this.readFileIntoStore} id="wallet_upload" className="hidden-file-input"/>
        <button className="btn" onClick={this.downloadWallet}>Download your wallet</button>
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
    this.setState({ toAddress: '', amount: '' });
    this.props.dispatch(actions.makeTransaction(this.state.toAddress, parseInt(this.state.amount), this.state.password));
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
  renderWalletButton() {
    if(!this.props.store.wallet.address) {
      return <button className="btn" onClick={this.generateWallet}>Generate New Wallet</button>;
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
